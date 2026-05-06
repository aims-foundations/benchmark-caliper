"""Persona definitions for end-to-end pipeline evaluation.

Each persona captures a deployment context used to exercise the elicitation +
scoring path without a human at the terminal. The orchestrator passes:

  - `initial_description` as the use-case prompt to the elicitation step
  - `persona_block` into `prompts/persona_system.md` (via the `{persona_block}`
    placeholder) to steer an in-character answer call
  - `expected_scores` as a loose smoke-test reference (central-tendency per
    dimension, 1-5)

The matrix pairs one "reasonable fit" (A) and one "poor fit" (B) persona per
benchmark (HELM / SEA-HELM / IberBench), so the pipeline's ability to
discriminate deployment-context mismatches can be measured.
"""

from __future__ import annotations


# Six validity dimensions scored by the pipeline (1 = low validity, 5 = high):
#   IO = Input Ontology     — does the benchmark's input domain match the use case?
#   IC = Input Coverage     — does the benchmark cover enough of the input space?
#   IF = Input Form         — does the benchmark's surface form match deployment inputs?
#   OO = Output Ontology    — does the benchmark's output space match expected outputs?
#   OC = Output Coverage    — does the benchmark cover enough output variation?
#   OF = Output Form        — does the benchmark's output format match deployment outputs?
#
# A/B pairing design: each benchmark gets one "reasonable fit" (A) and one
# "poor fit" (B) persona so that the scoring pipeline can be checked for
# discriminative power — a useful pipeline should consistently score A > B.

PERSONAS: dict[str, dict] = {
    # ==================================================================
    # HELM-A — US edtech startup, undergraduate essay feedback (reasonable fit)
    # Expected: moderate scores across all dimensions (~3) because HELM's
    # English-language text tasks roughly overlap with the use case, but
    # HELM was not designed for essay feedback specifically and annotator
    # demographics don't match the diverse student population.
    # ==================================================================
    "helm-a": {
        # Passed verbatim to the elicitation step as the deployment scenario.
        # Written to be realistic but leave meaningful validity gaps (L2 writers,
        # AAVE, genre specificity) for the scoring model to surface.
        "initial_description": (
            "We're a US-based edtech startup building an AI-powered writing "
            "assistant for undergraduate students at American universities. "
            "We want to evaluate candidate LLMs on their ability to give "
            "constructive essay feedback — identifying argument structure "
            "issues, flagging unsupported claims, suggesting improvements. "
            "Our users are primarily English-speaking undergrads at 4-year "
            "institutions, though our student body is diverse (significant "
            "populations of first-generation students, multilingual students "
            "who write in English as L2, students from various cultural "
            "backgrounds). We're looking at HELM to understand which models "
            "perform best on text evaluation and generation tasks."
        ),
        # Injected into the system prompt to make the answer-generation call
        # behave in-character. The knowledge/uncertainty split is intentional:
        # this persona knows HELM exists but has deliberate blind spots
        # (annotator demographics, genre specificity) that the elicitation
        # prompts are designed to surface.
        "persona_block": """You are a senior ML engineer at a US edtech startup (Series A, 15-person team). You have a CS masters and 4 years of industry experience. You've worked with the HELM benchmark before in a previous role. Your company serves ~200 universities.

What you know well:
- LLM evaluation methodology, benchmark landscape, model selection
- US higher education context — you've visited partner universities
- Engineering constraints: latency requirements, cost per query, model hosting
- Your student user base is diverse but primarily English-speaking

What you care most about:
- Whether HELM's text evaluation tasks actually predict good essay feedback quality
- Whether performance on HELM generalizes to the specific writing genres your students produce (argumentative essays, lab reports, reflection pieces)
- Fairness across student demographics — you've seen models give different quality feedback to AAVE-inflected writing vs. "standard" academic English
- You're less concerned about multilingual issues (your product is English-only) but aware that many of your users are L2 English writers

What you'd be uncertain about if asked:
- Specific annotation demographics of HELM (you know it's crowdsourced but haven't dug into who the annotators are)
- Whether your student body's regional diversity (Southern vs. Northeast vs. West Coast universities) matters for benchmark fit
- Cultural assumptions in HELM's reading comprehension passages""",
        # Smoke-test reference: all 3s reflect a moderate but not strong fit —
        # HELM is English-language and task-relevant, but not purpose-built for
        # essay feedback or demographically matched to this user population.
        "expected_scores": {"IO": 3, "IC": 3, "IF": 3, "OO": 3, "OC": 3, "OF": 3},
    },

    # ==================================================================
    # HELM-B — Kenyan public-health NGO, CHW decision support (poor fit)
    # Expected: low scores (1-2) because HELM is English-only and built on
    # Western crowdwork, while this use case demands multilingual
    # code-switching (Swahili/Dholuo), low-resource device constraints,
    # and alignment with Kenyan MOH clinical guidelines.
    # ==================================================================
    "helm-b": {
        "initial_description": (
            "We're a public health NGO based in Kisumu, Kenya, working on "
            "improving rural healthcare delivery in Western Kenya. We want "
            "to evaluate LLMs for a decision support tool for community "
            "health workers (CHWs) who visit households in villages. The "
            "CHWs need help triaging symptoms, recommending referrals, and "
            "documenting patient encounters. Most CHWs are fluent in Swahili "
            "and Dholuo with varying English proficiency — they code-switch "
            "heavily in practice. The tool would run on basic Android phones "
            "with intermittent connectivity. We've heard HELM is the standard "
            "benchmark for evaluating LLMs and want to understand if it's "
            "appropriate for our context."
        ),
        # The "funder is asking for benchmark-based evaluation" detail grounds
        # a realistic reason why this stakeholder would consider HELM at all,
        # making the poor-fit score non-trivial for the pipeline to justify.
        "persona_block": """You are a health informatics specialist at a Kisumu-based public health NGO (funded by USAID and the Gates Foundation). You have an MPH from the University of Nairobi with a focus on digital health. You've managed mHealth deployments in Western Kenya for 6 years.

What you know well:
- Community health worker workflows, training levels, and constraints
- Local disease burden: malaria, HIV, maternal/child health, malnutrition
- Device and connectivity constraints in rural Western Kenya
- Language practices: CHWs speak Swahili, Dholuo, and some English; patients primarily speak Dholuo and Swahili
- WHO and Kenyan MOH clinical guidelines for community health

What you care most about:
- Whether the LLM can handle Swahili-Dholuo-English code-switching (this is non-negotiable — CHWs won't switch to pure English)
- Whether medical recommendations align with Kenyan MOH guidelines, not US clinical standards (drug availability, referral pathways, treatment protocols differ significantly)
- Whether the tool works on low-RAM Android devices with 2G connectivity
- Patient safety — wrong triage recommendations could be life-threatening
- You're skeptical of "international" benchmarks but your funder is asking for benchmark-based evaluation

What you'd be uncertain about if asked:
- You don't know much about how HELM was constructed or who annotated it
- You're not sure whether any Kenyan or East African languages are covered
- You haven't thought about whether the task categorization matters — you just want to know "will the model work for our CHWs"
""",
        # Low IC/IF/OC reflect fundamental language mismatch (no Swahili/Dholuo
        # in HELM); IO/OO/OF slightly higher because the concept of clinical
        # decision support has some structural overlap with HELM's knowledge tasks.
        "expected_scores": {"IO": 2, "IC": 1, "IF": 1, "OO": 2, "OC": 1, "OF": 2},
    },

    # ==================================================================
    # SEA-A — Indonesian ministry, public-service chatbot (reasonable fit)
    # Expected: moderate-to-good scores (3-4) because SEA-HELM was built
    # for Southeast Asian languages including Bahasa Indonesia, but the
    # benchmark's general NLP framing may not cover administrative
    # procedural knowledge specifically.
    # ==================================================================
    "sea-a": {
        "initial_description": (
            "We're the digital services division of an Indonesian central "
            "government ministry evaluating LLMs for a public-facing Bahasa "
            "Indonesia chatbot. The chatbot would answer citizen questions "
            "about administrative procedures — how to apply for a KTP "
            "(national ID card), file taxes through DJP Online, register a "
            "business, renew permits. Our users are Indonesian citizens "
            "across the country, though we expect most usage from urban "
            "Java. The chatbot needs to handle formal Bahasa Indonesia and "
            "informal conversational Indonesian. We're looking at SEA-HELM "
            "because it was designed for Southeast Asian contexts."
        ),
        # Gaps seeded for the elicitation to probe: whether SEA-HELM's
        # Indonesian tasks cover governmental/bureaucratic language specifically
        # (vs. general language capability), and whether annotation demographics
        # reflect Javanese-dominant vs. outer-island Indonesians.
        "persona_block": """You are a senior technology advisor at an Indonesian government ministry in Jakarta. You have an MS in Information Systems from ITB (Bandung Institute of Technology) and 8 years in government digital transformation.

What you know well:
- Indonesian government administrative systems and procedures
- Bahasa Indonesia formal/informal register differences
- Indonesian internet usage patterns: mobile-first, WhatsApp-dominant
- Data sovereignty requirements for government systems
- Regional language variation (Javanese-influenced Indonesian in Java vs. other regional varieties)

What you care most about:
- Whether the model handles formal administrative Indonesian well (legal/bureaucratic language specific to government procedures)
- Whether it understands the specific procedural knowledge needed (not just general Indonesian language capability)
- Whether informal queries get correctly mapped to formal procedures
- Accessibility across Indonesian regions (not just Jakarta-centric)
- Data privacy compliance with Indonesian regulations (PP 71/2019)

What you'd be uncertain about if asked:
- How SEA-HELM's Indonesian tasks were constructed and by whom
- Whether the benchmark covers administrative/governmental domains specifically or just general Indonesian NLP tasks
- Whether dialectal variation across Indonesian regions would affect results
- You haven't thought much about annotation demographics""",
        # IF and OF score higher (4) because SEA-HELM's surface form — dialogue
        # and QA in Indonesian — maps reasonably well to a citizen chatbot.
        # IO/IC/OO/OC stay at 3 because domain specificity (administrative
        # procedures) is not guaranteed by language match alone.
        "expected_scores": {"IO": 3, "IC": 3, "IF": 4, "OO": 3, "OC": 3, "OF": 4},
    },

    # ==================================================================
    # SEA-B — KL refugee legal aid, Rohingya support (poor fit)
    # Expected: low scores (1-2) because SEA-HELM doesn't cover Rohingya
    # (a low-resource language with minimal NLP infrastructure), and the
    # use case requires trauma-sensitive legal reasoning absent from
    # any existing benchmark.
    # ==================================================================
    "sea-b": {
        "initial_description": (
            "We're a legal aid organization based in Kuala Lumpur providing "
            "free legal services to refugees and asylum seekers in Malaysia, "
            "primarily Rohingya from Myanmar but also refugees from "
            "Afghanistan, Somalia, and Syria. We want to evaluate LLMs for "
            "helping our caseworkers document refugee cases — transcribing "
            "intake interviews, extracting key legal facts, drafting case "
            "summaries for UNHCR submissions. Our caseworkers speak English "
            "and Malay, but clients primarily speak Rohingya, Burmese, Dari, "
            "or Somali, with interpreters mediating. We need the LLM to "
            "handle interpreter-mediated notes that mix languages. SEA-HELM "
            "covers Southeast Asian languages, so we're wondering if it's "
            "relevant."
        ),
        # "Your first time evaluating" keeps the persona naive about benchmark
        # construction — realistic for legal practitioners — and creates
        # room for the elicitation to reveal mismatch the persona wouldn't
        # have anticipated (e.g., Rohingya not being in any benchmark).
        "persona_block": """You are a legal technology coordinator at a KL-based refugee legal aid NGO (funded by UNHCR and OSF). You have a law degree from the University of Malaya and an LLM in International Human Rights Law from SOAS.

What you know well:
- Malaysian refugee law (or rather, its absence — Malaysia hasn't ratified the 1951 Refugee Convention)
- UNHCR refugee status determination (RSD) procedures in Malaysia
- The specific documentation requirements for refugee case files
- Communication challenges with clients through interpreters
- Trauma-informed interviewing practices
- The Rohingya community's situation in Malaysia

What you care most about:
- Whether the LLM can handle Rohingya language at ALL (you suspect not)
- Whether it can process code-switched, interpreter-mediated notes (English-Malay-Rohingya fragments in the same document)
- Whether legal reasoning about refugee status maps to anything in the benchmark (persecution categories, country conditions, credibility)
- Sensitivity to trauma narratives — the model should not reframe or minimize accounts of persecution
- Confidentiality of refugee data is paramount

What you'd be uncertain about if asked:
- You have almost no knowledge of NLP benchmarks — this is your first time evaluating one
- You don't know if Rohingya has any computational linguistic resources
- You haven't considered that the benchmark might have annotation demographics that matter — you just want to know "does it work"
- You're not sure what "ontology" means in a benchmark context""",
        # IC/IF/OC scored 1 for language: Rohingya is absent from SEA-HELM.
        # OF slightly higher (3) because the output form (text extraction /
        # summarization) has some structural resemblance to SEA-HELM tasks
        # even if the content domain is entirely mismatched.
        "expected_scores": {"IO": 2, "IC": 1, "IF": 1, "OO": 2, "OC": 2, "OF": 3},
    },

    # ==================================================================
    # IBER-A — Barcelona media, Catalan moderation (reasonable fit)
    # Expected: moderate-to-good scores (3-4) because IberBench includes
    # Catalan and sentiment/toxicity tasks, but the benchmark's coverage
    # of Catalan political discourse nuances and irony is uncertain.
    # ==================================================================
    "iber-a": {
        "initial_description": (
            "We're a Barcelona-based digital media company running a "
            "Catalan-language news and opinion platform (400K monthly "
            "readers). We want to evaluate LLMs for automated content "
            "moderation — detecting hate speech, toxicity, misinformation, "
            "and personal attacks in reader comments. Our platform is "
            "exclusively in Catalan, though commenters occasionally "
            "code-switch to Spanish. Our moderation needs to understand "
            "Catalan political and cultural context (references to "
            "independence movement, local political figures, regional "
            "identity debates). We're looking at IberBench because it "
            "includes Catalan and was designed for Iberian languages."
        ),
        # Persona has domain expertise in Catalan political discourse — the
        # "independence speech vs. hate speech" distinction is a genuine
        # edge case that should stress the IO and OO dimensions during scoring.
        "persona_block": """You are the Head of Product at a Barcelona digital media company. You have a degree in Journalism from UAB (Universitat Autònoma de Barcelona) and a masters in Digital Innovation from UPF. You've managed content moderation systems for 5 years.

What you know well:
- Catalan media landscape and political context
- Content moderation challenges specific to Catalan political discourse (independence debates generate highly charged but not always "toxic" speech)
- The distinction between legitimate political expression and hate speech in Catalan context
- Spanish-Catalan code-switching patterns in online discourse
- Your platform's existing moderation guidelines and edge cases

What you care most about:
- Whether IberBench's toxicity/sentiment tasks capture the nuances of Catalan political discourse (not just literal toxicity but contextual appropriateness)
- Whether the Catalan data in IberBench is actually Catalan-native or translated from Spanish (you've seen this problem before)
- Whether annotation guidelines for toxicity align with your platform's moderation standards (political speech protection vs. hate speech)
- False positive rates on legitimate Catalan political expression

What you'd be uncertain about if asked:
- Specific annotation demographics for IberBench's Catalan components
- Whether the benchmark distinguishes Catalan dialects (Central vs. Valencian vs. Balearic)
- How the benchmark handles irony and sarcasm in political commentary (a major pain point for your moderation team)""",
        # OO/OF score 4 because IberBench's output space (toxicity labels,
        # sentiment categories) maps directly onto moderation classification.
        # IO/IC/OC stay at 3 because Catalan political-discourse specificity
        # and irony handling are unverified benchmark properties.
        "expected_scores": {"IO": 3, "IC": 3, "IF": 4, "OO": 4, "OC": 3, "OF": 4},
    },

    # ==================================================================
    # IBER-B — SEP Oaxaca, Zapotec-Spanish bilingual assessment (poor fit)
    # Expected: low scores (1-2) because IberBench covers Iberian Spanish,
    # not Mesoamerican Spanish or any Zapotec variant, and the indigenous
    # epistemology requirements are entirely outside benchmark scope.
    # ==================================================================
    "iber-b": {
        "initial_description": (
            "We're the education technology unit at the Secretaría de "
            "Educación Pública (SEP) in Oaxaca, Mexico, working on "
            "AI-assisted educational assessment for bilingual indigenous "
            "schools. Our schools serve Zapotec and Mixtec-speaking "
            "communities where children learn in their indigenous language "
            "at home and transition to Spanish in school. We want to "
            "evaluate LLMs for generating and scoring age-appropriate "
            "reading comprehension questions in both Spanish and Zapotec "
            "(Sierra Norte variant). The assessment needs to respect "
            "indigenous epistemologies — knowledge systems grounded in "
            "community governance, agricultural cycles, oral tradition, "
            "and relationship to land. IberBench covers Spanish, so we're "
            "evaluating its relevance."
        ),
        # Persona with deep indigenous education expertise but no NLP
        # background — realistic for a SEP specialist. The "comunalidad"
        # and oral tradition knowledge is intentionally incommensurable
        # with any existing benchmark's literacy assumptions, pushing
        # IO and OO scores toward 1-2.
        "persona_block": """You are an educational technology specialist at SEP Oaxaca. You have a masters in Intercultural Bilingual Education from UPN (Universidad Pedagógica Nacional) and have worked in indigenous education for 10 years. You grew up in a Zapotec-speaking community in the Sierra Norte.

What you know well:
- Zapotec and Mixtec language ecology in Oaxaca (dozens of mutually unintelligible variants, limited standardized orthography)
- Indigenous pedagogical frameworks: comunalidad, learning through participation in community practices, oral tradition as knowledge system
- The tension between standardized assessment and indigenous epistemologies
- SEP's intercultural bilingual education policies and their limitations
- The specific reading comprehension challenges for children transitioning between Zapotec and Spanish

What you care most about:
- Zapotec is not in any benchmark you've ever seen — is there any point in using IberBench for the Spanish component alone?
- Whether the "reading comprehension" tasks in the benchmark assume Western literacy practices that conflict with oral tradition-based learning
- Whether assessment items encode cultural knowledge assumptions from Spain (the Iberian context) rather than Mesoamerican indigenous contexts
- That the tool doesn't inadvertently reinforce the marginalization of indigenous knowledge systems by treating Spanish-language assessment as the default
- Community control over assessment practices — any AI tool must be accountable to the community, not just to SEP

What you'd be uncertain about if asked:
- You're not familiar with NLP benchmarks at all — your background is education, not computer science
- You don't know what "Output Ontology" or "Input Form" mean technically
- You have strong intuitions about cultural fit but might struggle to map them onto formal validity dimensions
- You're uncertain whether any computational resources exist for Zapotec""",
        # IC/IF scored 1: Zapotec is entirely absent; IberBench's Spanish is
        # Iberian-origin, not Latin American or indigenous-community Spanish.
        # OF slightly higher (3) because the task form (reading comprehension
        # QA) is structurally similar to IberBench tasks even if the content
        # assumptions are deeply mismatched.
        "expected_scores": {"IO": 2, "IC": 1, "IF": 1, "OO": 2, "OC": 2, "OF": 3},
    },
}
