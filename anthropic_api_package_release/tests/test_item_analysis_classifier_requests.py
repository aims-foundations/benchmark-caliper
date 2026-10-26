"""Independent requests retain their evidence and enforce only their own contract."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from item_analysis.classify import classification_request
from item_analysis.schema import (
    ROSTER, classifier_labels_schema, join_context, validate_classifier_labels,
)


@pytest.fixture
def spec():
    context = json.loads((Path(__file__).parent / 'fixtures' / 'item_analysis_generic_context.json').read_text())
    registry = {
        'deployment_description.txt': context['deployment_description'],
        'scope.txt': 'Exclude foreign law examinations from this deployment.',
        'arithmetic.md': 'A quarter plus a quarter equals one half.',
        'scoring.md': 'Only the final numerical answer is scored.',
        'prior.txt': 'Earlier assessment suspects scoring does not reflect reasoning.',
        'unused.md': 'Unrelated benchmark documentation.',
    }
    roles = {
        'deployment_description.txt': 'deployment_requirement', 'scope.txt': 'deployment_requirement',
        'arithmetic.md': 'domain_evidence', 'scoring.md': 'benchmark_evidence',
        'prior.txt': 'prior_assessment', 'unused.md': 'benchmark_evidence',
    }
    context['context_by_classifier']['output_content']['benchmark_evidence'] = [
        {'statement': registry['arithmetic.md'], 'source_ids': ['arithmetic.md']},
    ]
    context['context_by_classifier']['output_ontology']['benchmark_evidence'] = [
        {'statement': registry['scoring.md'], 'source_ids': ['scoring.md']},
    ]
    context['context_by_classifier']['output_ontology']['prior_hypotheses'] = [
        {'statement': registry['prior.txt'], 'source_ids': ['prior.txt']},
    ]
    return join_context(context, profile={}, source_registry=registry, source_roles=roles)


def judgment(cid):
    value = {'label': 'no_issue_identified', 'evidence': ['content: 1/4 + 1/4'],
             'justification': 'The reference agrees with the supplied arithmetic standard.'}
    if cid == 'input_ontology':
        value.update(label='match', matched_category_ids=['math'], scope_exclusion_source_ids=[])
    return value


@pytest.mark.parametrize('cid', ROSTER)
def test_request_is_scoped_to_one_dimension_and_its_original_evidence(spec, cid):
    before = deepcopy(spec)
    item = {'item_id': 'fractions', 'content': '1/4 + 1/4', 'reference_answer': '1/2'}
    request = classification_request(item, spec, spec['deployment'], cid)
    payload = json.loads(request['user'])
    assert payload['classifier'] == next(c for c in spec['classifiers'] if c['id'] == cid)
    assert payload['context'] == spec['context_by_classifier'][cid]
    assert 'context_by_classifier' not in payload and 'classifiers' not in payload
    assert payload['item'] == item
    assert payload['output_schema']['properties']['labels']['required'] == [cid]
    assert ('input_category_inventory' in payload) == (cid == 'input_ontology')
    expected_sources = {'deployment_description.txt', 'scope.txt'}
    if cid == 'output_content':
        expected_sources.add('arithmetic.md')
    if cid == 'output_ontology':
        expected_sources.update({'scoring.md', 'prior.txt'})
    assert set(payload['source_registry']) == expected_sources
    assert payload['source_roles'] == {key: spec['source_roles'][key] for key in expected_sources}
    assert payload['source_registry'] == {key: spec['source_registry'][key] for key in expected_sources}
    assert request['step'] == f'item_classification.{cid}'
    assert spec == before


@pytest.mark.parametrize('cid', ROSTER)
def test_only_requested_judgment_is_accepted(spec, cid):
    response = {'labels': {cid: judgment(cid)}}
    assert validate_classifier_labels(response, spec, cid) == response['labels']
    sibling = next(key for key in ROSTER if key != cid)
    response['labels'][sibling] = judgment(sibling)
    with pytest.raises(ValueError):
        validate_classifier_labels(response, spec, cid)
    with pytest.raises(ValueError):
        validate_classifier_labels({'labels': {sibling: judgment(sibling)}}, spec, cid)


def test_partial_inventory_no_match_requires_a_real_deployment_exclusion(spec):
    label = judgment('input_ontology')
    label.update(label='no_match', matched_category_ids=[], scope_exclusion_source_ids=[])
    payload = {'labels': {'input_ontology': label}}
    with pytest.raises(ValueError):
        validate_classifier_labels(payload, spec, 'input_ontology')
    for source in ['invented.txt', 'arithmetic.md']:
        label['scope_exclusion_source_ids'] = [source]
        with pytest.raises(ValueError):
            validate_classifier_labels(payload, spec, 'input_ontology')
    label['scope_exclusion_source_ids'] = ['scope.txt']
    assert validate_classifier_labels(payload, spec, 'input_ontology')['input_ontology'] == label


@pytest.mark.parametrize('cid', ROSTER)
def test_missing_evidence_and_invalid_labels_are_rejected_per_classifier(spec, cid):
    label = judgment(cid)
    for field, value in [('label', 'probably_fine'), ('evidence', []), ('justification', ' ')]:
        invalid = {**label, field: value}
        with pytest.raises(ValueError):
            validate_classifier_labels({'labels': {cid: invalid}}, spec, cid)


def test_single_classifier_schema_does_not_mutate_or_relax_ontology_categories(spec):
    first = classifier_labels_schema(spec, 'input_ontology')
    classifier_labels_schema(spec, 'output_content')
    assert first['properties']['labels']['required'] == ['input_ontology']
    label = judgment('input_ontology')
    label['matched_category_ids'] = ['invented']
    with pytest.raises(ValueError):
        validate_classifier_labels({'labels': {'input_ontology': label}}, spec, 'input_ontology')
    with pytest.raises(ValueError):
        classifier_labels_schema(spec, 'invented_classifier')
