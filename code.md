# Repository Code Context
_Generated: 2025-09-06T21:17:43.553468Z_

## Directory Tree (depth ≤ 3)

```
configs/
  ├─ chunking.config.json
  ├─ eval.prompts.yaml
  ├─ metadata.dictionary.yaml
  ├─ normalization.rules.yaml
  ├─ sources.salesforce.yaml
data/
  ├─ final/
    ├─ dictionaries/
    ├─ inventory/
      ├─ salesforce_inventory.csv
    ├─ reports/
      ├─ day1_execution_report.json
      ├─ day1_verification.json
      ├─ link_health.json
      ├─ link_health_report.json
      ├─ link_health_summary.csv
    ├─ rules/
  ├─ interim/
    ├─ chunks/
      ├─ filtered/
      ├─ crm::10-K::2015-08-31::fy25-form-10-k::4c26cea2.chunks.jsonl
      ├─ crm::10-Q::2020-02-12::fy26-q1-10-q::e16f2866.chunks.jsonl
      ├─ crm::8-K::2025-01-31::8-k-fy25-results::d14102e8.chunks.jsonl
      ├─ crm::8-K::2025-04-30::8-k-q1-fy26-results::35792ff4.chunks.jsonl
      ├─ crm::8-K::2025-06-05::proxy-meeting-results-2025-06-05::47c09586.chunks.jsonl
      ├─ crm::dev_docs::2024-01-01::agentforce-agents-agentforce-developer-guide::5ac08bad.chunks.jsonl
      ├─ crm::dev_docs::2024-01-01::chat-with-agents-using-agent-api-agentforce-agents::6f4b900c.chunks.jsonl
      ├─ crm::dev_docs::2024-01-01::examples-agentforce-agents-agentforce-developer-gu::62fd6b36.chunks.jsonl
      ├─ crm::dev_docs::2024-01-01::get-started-agentforce-agents-agentforce-developer::202f14da.chunks.jsonl
      ├─ crm::help_docs::2024-09-05::salesforce-help::b0daabdf.chunks.jsonl
      ├─ crm::help_docs::2024-09-06::salesforce-help::b0daabdf.chunks.jsonl
      ├─ crm::press::2024-01-01::annual-reports::3814b366.chunks.jsonl
      ├─ crm::press::2024-01-01::board-of-directors::7ee63d65.chunks.jsonl
      ├─ crm::press::2024-01-01::events-and-presentations::0371587e.chunks.jsonl
      ├─ crm::press::2024-01-01::executive-management::2495a457.chunks.jsonl
      ├─ crm::press::2024-01-01::investor-contacts::54999c16.chunks.jsonl
      ├─ crm::press::2024-01-01::investor-email-alerts::626b16ec.chunks.jsonl
      ├─ crm::press::2024-01-01::investor-faqs::087af470.chunks.jsonl
      ├─ crm::press::2024-01-01::quarterly-results::11c603d4.chunks.jsonl
      ├─ crm::press::2024-01-01::sec-filings::7ec42ed9.chunks.jsonl
      ├─ crm::press::2024-01-01::stock-information::8ebb1472.chunks.jsonl
      ├─ crm::press::2024-02-28::salesforce-data-cloud::4ca56502.chunks.jsonl
      ├─ crm::press::2024-02-28::salesforce-legal::c00cb576.chunks.jsonl
      ├─ crm::press::2024-03-15::salesforce-integration::f0468619.chunks.jsonl
      ├─ crm::press::2024-04-18::salesforce-privacy::c517fb3f.chunks.jsonl
      ├─ crm::press::2024-04-25::salesforce-analytics::afc4c82e.chunks.jsonl
      ├─ crm::press::2024-05-25::salesforce-equality::874ae8c4.chunks.jsonl
      ├─ crm::press::2024-05-30::commerce-cloud::79bc8c33.chunks.jsonl
      ├─ crm::press::2024-06-20::sales-cloud::df3fdedd.chunks.jsonl
      ├─ crm::press::2024-06-30::salesforce-sustainability::d42ed8dd.chunks.jsonl
      ├─ crm::press::2024-07-15::service-cloud::a246d582.chunks.jsonl
      ├─ crm::press::2024-07-20::salesforce-leadership::5fe0d7a5.chunks.jsonl
      ├─ crm::press::2024-08-10::marketing-cloud::7ce342b2.chunks.jsonl
      ├─ crm::press::2024-08-15::salesforce-careers::4964b777.chunks.jsonl
      ├─ crm::press::2024-09-05::salesforce-platform::a8686c16.chunks.jsonl
      ├─ crm::press::2024-09-12::about-salesforce-company::3ae394fc.chunks.jsonl
      ├─ crm::press::2025-02-23::environmental-social-and-governance-esg::d4f786ad.chunks.jsonl
      ├─ crm::press::2025-02-25::corporate-governance::0ec4193a.chunks.jsonl
      ├─ crm::press::2025-08-26::newsroom::39cb1c1e.chunks.jsonl
      ├─ crm::press::None::news::6335e2de.chunks.jsonl
      ├─ crm::product::2024-01-01::agentforce-the-ai-agent-platform::5d10c49a.chunks.jsonl
      ├─ crm::product::2024-01-01::salesforce-data-cloud::04dae357.chunks.jsonl
      ├─ crm::product::2024-01-01::what-is-salesforce::17018047.chunks.jsonl
      ├─ crm::wiki::2025-09-05::salesforce::6b727edd.chunks.jsonl
      ├─ crm::wiki::2025-09-06::salesforce::6b727edd.chunks.jsonl
    ├─ dedup/
      ├─ dedup_map.json
    ├─ eval/
      ├─ salesforce_eval_seed.jsonl
    ├─ normalized/
      ├─ crm::10-K::2015-08-31::fy25-form-10-k::4c26cea2.json
      ├─ crm::10-Q::2020-02-12::fy26-q1-10-q::e16f2866.json
      ├─ crm::8-K::2025-01-31::8-k-fy25-results::d14102e8.json
      ├─ crm::8-K::2025-04-30::8-k-q1-fy26-results::35792ff4.json
      ├─ crm::8-K::2025-06-05::proxy-meeting-results-2025-06-05::47c09586.json
      ├─ crm::dev_docs::2024-01-01::agentforce-agents-agentforce-developer-guide::5ac08bad.json
      ├─ crm::dev_docs::2024-01-01::chat-with-agents-using-agent-api-agentforce-agents::6f4b900c.json
      ├─ crm::dev_docs::2024-01-01::examples-agentforce-agents-agentforce-developer-gu::62fd6b36.json
      ├─ crm::dev_docs::2024-01-01::get-started-agentforce-agents-agentforce-developer::202f14da.json
      ├─ crm::help_docs::2024-09-05::salesforce-help::b0daabdf.json
      ├─ crm::help_docs::2024-09-06::salesforce-help::b0daabdf.json
      ├─ crm::press::2024-01-01::annual-reports::3814b366.json
      ├─ crm::press::2024-01-01::board-of-directors::7ee63d65.json
      ├─ crm::press::2024-01-01::events-and-presentations::0371587e.json
      ├─ crm::press::2024-01-01::executive-management::2495a457.json
      ├─ crm::press::2024-01-01::investor-contacts::54999c16.json
      ├─ crm::press::2024-01-01::investor-email-alerts::626b16ec.json
      ├─ crm::press::2024-01-01::investor-faqs::087af470.json
      ├─ crm::press::2024-01-01::quarterly-results::11c603d4.json
      ├─ crm::press::2024-01-01::sec-filings::7ec42ed9.json
      ├─ crm::press::2024-01-01::stock-information::8ebb1472.json
      ├─ crm::press::2024-02-28::salesforce-data-cloud::4ca56502.json
      ├─ crm::press::2024-02-28::salesforce-legal::c00cb576.json
      ├─ crm::press::2024-03-15::salesforce-integration::f0468619.json
      ├─ crm::press::2024-04-18::salesforce-privacy::c517fb3f.json
      ├─ crm::press::2024-04-25::salesforce-analytics::afc4c82e.json
      ├─ crm::press::2024-05-25::salesforce-equality::874ae8c4.json
      ├─ crm::press::2024-05-30::commerce-cloud::79bc8c33.json
      ├─ crm::press::2024-06-20::sales-cloud::df3fdedd.json
      ├─ crm::press::2024-06-30::salesforce-sustainability::d42ed8dd.json
      ├─ crm::press::2024-07-15::service-cloud::a246d582.json
      ├─ crm::press::2024-07-20::salesforce-leadership::5fe0d7a5.json
      ├─ crm::press::2024-08-10::marketing-cloud::7ce342b2.json
      ├─ crm::press::2024-08-15::salesforce-careers::4964b777.json
      ├─ crm::press::2024-09-05::salesforce-platform::a8686c16.json
      ├─ crm::press::2024-09-12::about-salesforce-company::3ae394fc.json
      ├─ crm::press::2025-02-23::environmental-social-and-governance-esg::d4f786ad.json
      ├─ crm::press::2025-02-25::corporate-governance::0ec4193a.json
      ├─ crm::press::2025-08-26::newsroom::39cb1c1e.json
      ├─ crm::press::None::news::6335e2de.json
      ├─ crm::product::2024-01-01::agentforce-the-ai-agent-platform::5d10c49a.json
      ├─ crm::product::2024-01-01::salesforce-data-cloud::04dae357.json
      ├─ crm::product::2024-01-01::what-is-salesforce::17018047.json
      ├─ crm::wiki::2025-09-05::salesforce::6b727edd.json
      ├─ crm::wiki::2025-09-06::salesforce::6b727edd.json
  ├─ raw/
    ├─ dev_docs/
      ├─ crm::dev_docs::2024-01-01::agentforce-agents-agentforce-developer-guide::5ac08bad.meta.json
      ├─ crm::dev_docs::2024-01-01::agentforce-agents-agentforce-developer-guide::5ac08bad.raw.html
      ├─ crm::dev_docs::2024-01-01::chat-with-agents-using-agent-api-agentforce-agents::6f4b900c.meta.json
      ├─ crm::dev_docs::2024-01-01::chat-with-agents-using-agent-api-agentforce-agents::6f4b900c.raw.html
      ├─ crm::dev_docs::2024-01-01::examples-agentforce-agents-agentforce-developer-gu::62fd6b36.meta.json
      ├─ crm::dev_docs::2024-01-01::examples-agentforce-agents-agentforce-developer-gu::62fd6b36.raw.html
      ├─ crm::dev_docs::2024-01-01::get-started-agentforce-agents-agentforce-developer::202f14da.meta.json
      ├─ crm::dev_docs::2024-01-01::get-started-agentforce-agents-agentforce-developer::202f14da.raw.html
    ├─ help_docs/
      ├─ crm::help_docs::2024-09-05::salesforce-help::b0daabdf.meta.json
      ├─ crm::help_docs::2024-09-05::salesforce-help::b0daabdf.raw.html
      ├─ crm::help_docs::2024-09-06::salesforce-help::b0daabdf.meta.json
      ├─ crm::help_docs::2024-09-06::salesforce-help::b0daabdf.raw.html
    ├─ investor_news/
      ├─ crm::press::2024-01-01::annual-reports::3814b366.meta.json
      ├─ crm::press::2024-01-01::annual-reports::3814b366.raw.html
      ├─ crm::press::2024-01-01::board-of-directors::7ee63d65.meta.json
      ├─ crm::press::2024-01-01::board-of-directors::7ee63d65.raw.html
      ├─ crm::press::2024-01-01::events-and-presentations::0371587e.meta.json
      ├─ crm::press::2024-01-01::events-and-presentations::0371587e.raw.html
      ├─ crm::press::2024-01-01::executive-management::2495a457.meta.json
      ├─ crm::press::2024-01-01::executive-management::2495a457.raw.html
      ├─ crm::press::2024-01-01::investor-contacts::54999c16.meta.json
      ├─ crm::press::2024-01-01::investor-contacts::54999c16.raw.html
      ├─ crm::press::2024-01-01::investor-email-alerts::626b16ec.meta.json
      ├─ crm::press::2024-01-01::investor-email-alerts::626b16ec.raw.html
      ├─ crm::press::2024-01-01::investor-faqs::087af470.meta.json
      ├─ crm::press::2024-01-01::investor-faqs::087af470.raw.html
      ├─ crm::press::2024-01-01::quarterly-results::11c603d4.meta.json
      ├─ crm::press::2024-01-01::quarterly-results::11c603d4.raw.html
      ├─ crm::press::2024-01-01::sec-filings::7ec42ed9.meta.json
      ├─ crm::press::2024-01-01::sec-filings::7ec42ed9.raw.html
      ├─ crm::press::2024-01-01::stock-information::8ebb1472.meta.json
      ├─ crm::press::2024-01-01::stock-information::8ebb1472.raw.html
      ├─ crm::press::2025-02-23::environmental-social-and-governance-esg::d4f786ad.meta.json
      ├─ crm::press::2025-02-23::environmental-social-and-governance-esg::d4f786ad.raw.html
      ├─ crm::press::2025-02-25::corporate-governance::0ec4193a.meta.json
      ├─ crm::press::2025-02-25::corporate-governance::0ec4193a.raw.html
      ├─ crm::press::2025-08-26::newsroom::39cb1c1e.meta.json
      ├─ crm::press::2025-08-26::newsroom::39cb1c1e.raw.html
      ├─ crm::press::None::news::6335e2de.meta.json
      ├─ crm::press::None::news::6335e2de.raw.html
    ├─ newsroom/
      ├─ crm::press::2024-02-28::salesforce-data-cloud::4ca56502.meta.json
      ├─ crm::press::2024-02-28::salesforce-data-cloud::4ca56502.raw.html
      ├─ crm::press::2024-02-28::salesforce-legal::c00cb576.meta.json
      ├─ crm::press::2024-02-28::salesforce-legal::c00cb576.raw.html
      ├─ crm::press::2024-03-15::salesforce-integration::f0468619.meta.json
      ├─ crm::press::2024-03-15::salesforce-integration::f0468619.raw.html
      ├─ crm::press::2024-04-18::salesforce-privacy::c517fb3f.meta.json
      ├─ crm::press::2024-04-18::salesforce-privacy::c517fb3f.raw.html
      ├─ crm::press::2024-04-25::salesforce-analytics::afc4c82e.meta.json
      ├─ crm::press::2024-04-25::salesforce-analytics::afc4c82e.raw.html
      ├─ crm::press::2024-05-25::salesforce-equality::874ae8c4.meta.json
      ├─ crm::press::2024-05-25::salesforce-equality::874ae8c4.raw.html
      ├─ crm::press::2024-05-30::commerce-cloud::79bc8c33.meta.json
      ├─ crm::press::2024-05-30::commerce-cloud::79bc8c33.raw.html
      ├─ crm::press::2024-06-20::sales-cloud::df3fdedd.meta.json
      ├─ crm::press::2024-06-20::sales-cloud::df3fdedd.raw.html
      ├─ crm::press::2024-06-30::salesforce-sustainability::d42ed8dd.meta.json
      ├─ crm::press::2024-06-30::salesforce-sustainability::d42ed8dd.raw.html
      ├─ crm::press::2024-07-15::service-cloud::a246d582.meta.json
      ├─ crm::press::2024-07-15::service-cloud::a246d582.raw.html
      ├─ crm::press::2024-07-20::salesforce-leadership::5fe0d7a5.meta.json
      ├─ crm::press::2024-07-20::salesforce-leadership::5fe0d7a5.raw.html
      ├─ crm::press::2024-08-10::marketing-cloud::7ce342b2.meta.json
      ├─ crm::press::2024-08-10::marketing-cloud::7ce342b2.raw.html
      ├─ crm::press::2024-08-15::salesforce-careers::4964b777.meta.json
      ├─ crm::press::2024-08-15::salesforce-careers::4964b777.raw.html
      ├─ crm::press::2024-09-05::salesforce-platform::a8686c16.meta.json
      ├─ crm::press::2024-09-05::salesforce-platform::a8686c16.raw.html
      ├─ crm::press::2024-09-12::about-salesforce-company::3ae394fc.meta.json
      ├─ crm::press::2024-09-12::about-salesforce-company::3ae394fc.raw.html
    ├─ product/
      ├─ crm::product::2024-01-01::agentforce-the-ai-agent-platform::5d10c49a.meta.json
      ├─ crm::product::2024-01-01::agentforce-the-ai-agent-platform::5d10c49a.raw.html
      ├─ crm::product::2024-01-01::salesforce-data-cloud::04dae357.meta.json
      ├─ crm::product::2024-01-01::salesforce-data-cloud::04dae357.raw.html
      ├─ crm::product::2024-01-01::what-is-salesforce::17018047.meta.json
      ├─ crm::product::2024-01-01::what-is-salesforce::17018047.raw.html
    ├─ sec/
      ├─ crm::10-K::2015-08-31::fy25-form-10-k::4c26cea2.meta.json
      ├─ crm::10-K::2015-08-31::fy25-form-10-k::4c26cea2.raw.html
      ├─ crm::10-Q::2020-02-12::fy26-q1-10-q::e16f2866.meta.json
      ├─ crm::10-Q::2020-02-12::fy26-q1-10-q::e16f2866.raw.html
      ├─ crm::8-K::2025-01-31::8-k-fy25-results::d14102e8.meta.json
      ├─ crm::8-K::2025-01-31::8-k-fy25-results::d14102e8.raw.html
      ├─ crm::8-K::2025-04-30::8-k-q1-fy26-results::35792ff4.meta.json
      ├─ crm::8-K::2025-04-30::8-k-q1-fy26-results::35792ff4.raw.html
      ├─ crm::8-K::2025-06-05::proxy-meeting-results-2025-06-05::47c09586.meta.json
      ├─ crm::8-K::2025-06-05::proxy-meeting-results-2025-06-05::47c09586.raw.html
      ├─ crm::ars_pdf::2025-03-05::fy25-annual-report-pdf::1b31e86f.meta.json
      ├─ crm::ars_pdf::2025-03-05::fy25-annual-report-pdf::1b31e86f.raw.pdf
    ├─ wikipedia/
      ├─ crm::wiki::2025-09-05::salesforce::6b727edd.meta.json
      ├─ crm::wiki::2025-09-05::salesforce::6b727edd.raw.html
      ├─ crm::wiki::2025-09-06::salesforce::6b727edd.meta.json
      ├─ crm::wiki::2025-09-06::salesforce::6b727edd.raw.html
diagnostics/
  ├─ environment/
    ├─ env.json
    ├─ pip_freeze.txt
  ├─ runs/
    ├─ run_20250906_201833/
      ├─ py__qa_common/
      ├─ py_build_eval_seed/
      ├─ py_link_health_check/
      ├─ py_qa_boilerplate_mine/
      ├─ py_qa_chunk_quality/
      ├─ py_qa_coverage_report/
      ├─ py_qa_dedupe_audit/
      ├─ py_qa_eval_seed_validate/
      ├─ py_qa_ground_truth_builder/
      ├─ py_qa_link_health_retest/
      ├─ py_qa_manual_samples/
      ├─ py_qa_metadata_validate/
      ├─ py_qa_persona_tag_precision/
      ├─ py_qa_regression_pack/
      ├─ py_qa_schema_validate/
      ├─ py_qa_sec_section_validate/
      ├─ py_qa_text_quality/
      ├─ py_qa_verification_gate/
      ├─ py_verify_day1_milestones/
      ├─ summary.json
    ├─ run_20250906_211705/
      ├─ py__qa_common/
      ├─ py_build_eval_seed/
      ├─ py_link_health_check/
      ├─ py_qa_boilerplate_mine/
      ├─ py_qa_chunk_quality/
      ├─ py_qa_coverage_report/
      ├─ py_qa_dedupe_audit/
      ├─ py_qa_eval_seed_validate/
      ├─ py_qa_ground_truth_builder/
      ├─ py_qa_link_health_retest/
      ├─ py_qa_manual_samples/
      ├─ py_qa_metadata_validate/
      ├─ py_qa_persona_tag_precision/
      ├─ py_qa_regression_pack/
      ├─ py_qa_schema_validate/
      ├─ py_qa_sec_section_validate/
      ├─ py_qa_text_quality/
      ├─ py_qa_verification_gate/
      ├─ py_verify_day1_milestones/
      ├─ summary.json
    ├─ summary.latest.json
  ├─ diagnostic_bundle.json
gpt/
  ├─ ChatGPT-Branch · pro-ag1-data eval.md
logs/
  ├─ chunk/
    ├─ 20250906_171703.log
  ├─ dedupe/
    ├─ 20250906_171703.log
  ├─ eval/
    ├─ 20250906_161845.log
    ├─ 20250906_171705.log
    ├─ 20250906_171725.log
  ├─ normalize/
    ├─ 20250906_135744.log
    ├─ 20250906_135752.log
    ├─ 20250906_135753.log
    ├─ 20250906_140033.log
    ├─ 20250906_140131.log
    ├─ 20250906_140139.log
    ├─ 20250906_140350.log
    ├─ 20250906_140353.log
    ├─ 20250906_140435.log
    ├─ 20250906_142628.log
    ├─ 20250906_142641.log
    ├─ 20250906_142728.log
    ├─ 20250906_142755.log
    ├─ 20250906_161845.log
    ├─ 20250906_171725.log
  ├─ qa/
    ├─ qa_boilerplate_mine/
      ├─ 20250906_161835.log
      ├─ 20250906_171707.log
    ├─ qa_chunk_quality/
      ├─ 20250906_161842.log
      ├─ 20250906_171714.log
    ├─ qa_coverage_report/
      ├─ 20250906_161842.log
      ├─ 20250906_171714.log
    ├─ qa_dedupe_audit/
      ├─ 20250906_161843.log
      ├─ 20250906_171715.log
    ├─ qa_eval_seed_validate/
      ├─ 20250906_161845.log
      ├─ 20250906_171724.log
    ├─ qa_ground_truth_builder/
      ├─ 20250906_131020.log
      ├─ 20250906_131155.log
      ├─ 20250906_131325.log
      ├─ 20250906_140033.log
      ├─ 20250906_140148.log
      ├─ 20250906_140405.log
      ├─ 20250906_142654.log
      ├─ 20250906_161844.log
      ├─ 20250906_171724.log
    ├─ qa_link_health_retest/
      ├─ 20250906_161835.log
      ├─ 20250906_171708.log
    ├─ qa_manual_samples/
      ├─ 20250906_161843.log
      ├─ 20250906_171715.log
    ├─ qa_metadata_validate/
      ├─ 20250906_131156.log
      ├─ 20250906_131325.log
      ├─ 20250906_135820.log
      ├─ 20250906_140034.log
      ├─ 20250906_140148.log
      ├─ 20250906_140242.log
      ├─ 20250906_140303.log
      ├─ 20250906_140405.log
      ├─ 20250906_140436.log
      ├─ 20250906_142655.log
      ├─ 20250906_142807.log
      ├─ 20250906_161845.log
      ├─ 20250906_171724.log
    ├─ qa_persona_tag_precision/
      ├─ 20250906_161844.log
      ├─ 20250906_171723.log
    ├─ qa_regression_pack/
      ├─ 20250906_161842.log
      ├─ 20250906_171714.log
    ├─ qa_schema_validate/
      ├─ 20250906_131156.log
      ├─ 20250906_131325.log
      ├─ 20250906_135820.log
      ├─ 20250906_140034.log
      ├─ 20250906_140148.log
      ├─ 20250906_140405.log
      ├─ 20250906_140436.log
      ├─ 20250906_142655.log
      ├─ 20250906_142807.log
      ├─ 20250906_161835.log
      ├─ 20250906_171707.log
    ├─ qa_sec_section_validate/
      ├─ 20250906_161844.log
      ├─ 20250906_171723.log
    ├─ qa_text_quality/
      ├─ 20250906_161834.log
      ├─ 20250906_171706.log
    ├─ qa_verification_gate/
      ├─ 20250906_142655.log
      ├─ 20250906_161843.log
      ├─ 20250906_171715.log
qa_configs/
  ├─ qa.boilerplate.allowlist.txt
  ├─ qa.sec.sections.yaml
  ├─ qa.sources.baselines.yaml
  ├─ qa.thresholds.yaml
qa_data/
  ├─ baselines/
    ├─ ground_truth_dates.csv
    ├─ newsroom_rss_dates.csv
  ├─ outputs/
    ├─ boilerplate_signatures.json
    ├─ chunk_quality_report.json
    ├─ coverage_report.json
    ├─ dedupe_audit.json
    ├─ eval_seed_report.json
    ├─ link_health_retest.json
    ├─ metadata_report.json
    ├─ persona_tag_precision.json
    ├─ regression_pack.json
    ├─ schema_report.json
    ├─ sec_section_report.json
    ├─ text_quality_report.json
    ├─ verification_gate.json
  ├─ samples/
    ├─ manual_review_samples/
      ├─ chunks_for_review.csv
      ├─ docs_for_review.csv
qa_scripts/
  ├─ _qa_common.py
  ├─ generate_code_md.py
  ├─ make_diagnostic_bundle.py
  ├─ qa_boilerplate_mine.py
  ├─ qa_chunk_quality.py
  ├─ qa_coverage_report.py
  ├─ qa_dedupe_audit.py
  ├─ qa_eval_seed_validate.py
  ├─ qa_ground_truth_builder.py
  ├─ qa_link_health_retest.py
  ├─ qa_manual_samples.py
  ├─ qa_metadata_validate.py
  ├─ qa_persona_tag_precision.py
  ├─ qa_regression_pack.py
  ├─ qa_schema_validate.py
  ├─ qa_sec_section_validate.py
  ├─ qa_text_quality.py
  ├─ qa_verification_gate.py
  ├─ run_evals_and_collect.py
scripts/
  ├─ _common.py
  ├─ build_eval_seed.py
  ├─ chunk_documents.py
  ├─ dedupe_chunks.py
  ├─ extract_metadata.py
  ├─ fetch_dev_docs.py
  ├─ fetch_help_docs.py
  ├─ fetch_investor_news.py
  ├─ fetch_newsroom_index.py
  ├─ fetch_newsroom_rss.py
  ├─ fetch_product_docs.py
  ├─ fetch_sec_filings.py
  ├─ fetch_wikipedia.py
  ├─ link_health_check.py
  ├─ normalize_html.py
  ├─ parse_sec_structures.py
  ├─ verify_day1_milestones.py
.gitignore
code.md
PIPELINE_EXPLAINER.md
README_DAY1.md
requirements.txt
```

## Key Script Modules & Entry Points

### `/Users/liyunxiao/ag1-1/qa_scripts/_qa_common.py`
- Imports: _common, datetime, glob, json, logging, math, os, random, re, sys, typing
- Functions: qa_logger, ensure_parent, write_report, list_json_files, printable_ratio, count_replacement_char, stopword_ratio, char_bigram_entropy, mean, month_bucket, load_chunks_from_jsonl, overlap_tokens
- Classes: 
- Entry point: False

### `/Users/liyunxiao/ag1-1/qa_scripts/generate_code_md.py`
- Imports: ast, datetime, os, pathlib, re, sys
- Functions: list_tree, summarize_python_file, collect_configs, main, walk
- Classes: 
- Entry point: True

### `/Users/liyunxiao/ag1-1/qa_scripts/make_diagnostic_bundle.py`
- Imports: csv, datetime, json, os, pathlib, sys
- Functions: read_json, csv_rows, try_read_text, latest_run_summary, gather_env, gather_dataset, auto_flags, main
- Classes: 
- Entry point: True

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_boilerplate_mine.py`
- Imports: _qa_common, argparse, collections, glob, json, os, re
- Functions: extract_spans, main
- Classes: 
- Entry point: True
- CLI flags detected: --chunks-glob --doctype-filter --min_doc_freq --min_docs_for_boilerplate --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_chunk_quality.py`
- Imports: _common, _qa_common, argparse, glob, json, os, statistics
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --cfg --chunks-glob --fail-on --filtered-glob --limit --norm-glob --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_coverage_report.py`
- Imports: _common, _qa_common, argparse, datetime, glob, json, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --norm-glob --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_dedupe_audit.py`
- Imports: _qa_common, argparse, collections, glob, json, os, re
- Functions: load_dedup_map, grid_eval, main
- Classes: 
- Entry point: True
- CLI flags detected: --boilerplate --chunks-glob --dedup-map --limit --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_eval_seed_validate.py`
- Imports: _qa_common, argparse, collections, glob, json, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --chunks-glob --eval-path --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_ground_truth_builder.py`
- Imports: _common, _qa_common, argparse, csv, glob, os, re, scripts._common, typing
- Functions: parse_filed_date_from_html, main
- Classes: 
- Entry point: True
- CLI flags detected: --limit --out-dates --out-rss --raw-root

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_link_health_retest.py`
- Imports: _common, _qa_common, argparse, glob, json, os, random
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --link-report --norm-glob --out --sample-frac

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_manual_samples.py`
- Imports: _common, _qa_common, argparse, collections, csv, glob, json, os, random
- Functions: main, add_fails
- Classes: 
- Entry point: True
- CLI flags detected: --chunks-glob --norm-glob --out-chunks --out-docs --reports-root

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_metadata_validate.py`
- Imports: _common, _qa_common, argparse, csv, json, os, re, typing
- Functions: read_baselines, main
- Classes: 
- Entry point: True
- CLI flags detected: --baselines --cfg --fail-on --input-glob --limit --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_persona_tag_precision.py`
- Imports: _common, _qa_common, argparse, glob, json, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --norm-glob --out --prompts

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_regression_pack.py`
- Imports: _qa_common, argparse, json, os
- Functions: load, main
- Classes: 
- Entry point: True
- CLI flags detected: --curr-root --out --prev-root

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_schema_validate.py`
- Imports: _common, _qa_common, argparse, json, os, re, typing
- Functions: validate_doc, main
- Classes: 
- Entry point: True
- CLI flags detected: --fail-on --input-glob --limit --out --schema

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_sec_section_validate.py`
- Imports: _common, _qa_common, argparse, glob, json, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --cfg --norm-glob --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_text_quality.py`
- Imports: _common, _qa_common, argparse, json, os, typing
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --chunks-glob --fail-on --input-glob --limit --out

### `/Users/liyunxiao/ag1-1/qa_scripts/qa_verification_gate.py`
- Imports: _common, _qa_common, argparse, json, os
- Functions: load_json, main
- Classes: 
- Entry point: True
- CLI flags detected: --out --reports-root --thresholds

### `/Users/liyunxiao/ag1-1/qa_scripts/run_evals_and_collect.py`
- Imports: datetime, json, os, pathlib, re, subprocess, sys, time
- Functions: safe_cmd, detect_py_scripts, check_module_available, run_python_script, main
- Classes: 
- Entry point: True

### `/Users/liyunxiao/ag1-1/scripts/_common.py`
- Imports: atexit, bs4, datetime, dateutil, errno, feedparser, hashlib, json, langdetect, logging, math, os
- Functions: ensure_dir, ensure_parent, now_ts, ts_for_log, setup_logger, parse_iso_date, date_to_iso, clean_url_params, source_domain, slugify, sha1_8, sha256_hex
- Classes: RateLimiter
- Entry point: False

### `/Users/liyunxiao/ag1-1/scripts/build_eval_seed.py`
- Imports: _common, argparse, datetime, glob, json, os, random
- Functions: pick_keyphrases, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/chunk_documents.py`
- Imports: _common, argparse, glob, json, os
- Functions: chunk_text, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/dedupe_chunks.py`
- Imports: _common, argparse, collections, glob, json, os, re
- Functions: normalize_for_shingles, shingles, jaccard, main, doc_key
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/extract_metadata.py`
- Imports: _common, argparse, datetime, glob, os, re, urllib.parse
- Functions: load_topic_lexicon, apply_topics, apply_personas, backfill_publish_date, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_dev_docs.py`
- Imports: _common, argparse, datetime, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_help_docs.py`
- Imports: _common, argparse, datetime, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_investor_news.py`
- Imports: _common, argparse, datetime, os, re, urllib.parse
- Functions: discover_article_links, extract_visible_date, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_newsroom_index.py`
- Imports: _common, argparse, datetime, os, re, urllib.parse
- Functions: discover_links, extract_visible_date, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_newsroom_rss.py`
- Imports: _common, argparse, datetime, feedparser, os, re
- Functions: main, eget, entry_date
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_product_docs.py`
- Imports: _common, argparse, datetime, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_sec_filings.py`
- Imports: _common, argparse, datetime, os, re
- Functions: parse_filed_date, infer_doctype, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/fetch_wikipedia.py`
- Imports: _common, argparse, datetime, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/link_health_check.py`
- Imports: _common, argparse, glob, json, os, time
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/normalize_html.py`
- Imports: _common, argparse, datetime, glob, json, os, pdfminer.high_level
- Functions: normalized_path, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/parse_sec_structures.py`
- Imports: _common, argparse, glob, os, re
- Functions: find_spans, main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until

### `/Users/liyunxiao/ag1-1/scripts/verify_day1_milestones.py`
- Imports: _common, argparse, datetime, glob, json, os
- Functions: main
- Classes: 
- Entry point: True
- CLI flags detected: --concurrency --dry-run --limit --since --until


## Config Files Summary

- `/Users/liyunxiao/ag1-1/configs/metadata.dictionary.yaml` (size: 1854 bytes) sample keys: allowed, byline, company, default, description, doc_id, doctype, fields, fill_rule_precedence, final_url, full_domain, hash_sha256, html_title, ingestion_ts, language, last_modified_http, meta_published_time, optional_fields, owner, owner_script
- `/Users/liyunxiao/ag1-1/configs/normalization.rules.yaml` (size: 1145 bytes) sample keys: convert_infobox_to_text, drop_non_english, drop_repeated_nav_lists, drop_selectors, expected, global, investor_news, item_headers, keep_lead_and_first_three_headings, keep_toc_titles, language, newsroom, normalize, preserve_containers, product_dev_help, publish_date_source_order, sec, version, wikipedia
- `/Users/liyunxiao/ag1-1/configs/eval.prompts.yaml` (size: 729 bytes) sample keys: Agentforce, Earnings, Partnership, Product, cio, keywords, personas, topic_lexicon, version, vp_customer_experience, vp_sales_ops
- `/Users/liyunxiao/ag1-1/configs/chunking.config.json` (size: 190 bytes) sample keys: 
- `/Users/liyunxiao/ag1-1/configs/sources.salesforce.yaml` (size: 2137 bytes) sample keys: cap_pages, company, description, dev_docs, doctype_hints, feeds, help_docs, investor_news, newsroom_rss, product, sec, since, sources, start_url, target_count, target_count_total, url, urls, version, wikipedia
- `/Users/liyunxiao/ag1-1/qa_configs/qa.thresholds.yaml` (size: 867 bytes) sample keys: baseline_coverage_rate_overall_min, baseline_coverage_rate_press_sec_min, char_bigram_entropy_range, chunk_len_range_tokens, chunk_len_within_pct_min, chunk_median_range_tokens, date_match_rate_min, dup_rate_post_boilerplate_max, eval_distribution_min, eval_seed_integrity_required, exact_doc_dup_rate_max, fallback_any_rate_overall_max, fallback_today_rate_overall_max, language_prob_en_min, link_health_required, overlap_mean_range_tokens, per_persona, persona_precision_min, press, printable_ratio_min
- `/Users/liyunxiao/ag1-1/qa_configs/qa.sec.sections.yaml` (size: 100 bytes) sample keys: required_items, version
- `/Users/liyunxiao/ag1-1/qa_configs/qa.sources.baselines.yaml` (size: 941 bytes) sample keys: allow_domains, date_methods, dev_docs, help_docs, investor_news, newsroom, product, sec, sources, title_methods, version, wiki

## Data & Reports Present

- data/final/inventory/salesforce_inventory.csv: FOUND
- data/final/reports/day1_verification.json: FOUND
- data/final/reports/link_health.json: FOUND
- data/interim/dedup/dedup_map.json: FOUND
- data/interim/eval/salesforce_eval_seed.jsonl: FOUND