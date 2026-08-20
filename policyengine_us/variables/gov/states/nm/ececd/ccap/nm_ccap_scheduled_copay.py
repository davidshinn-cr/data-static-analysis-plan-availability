from policyengine_us.model_api import *


class nm_ccap_scheduled_copay(Variable):
    value_type = float
    entity = SPMUnit
    unit = USD
    definition_period = MONTH
    label = "New Mexico CCAP copayment from the published schedule"
    defined_for = StateCode.NM
    reference = (
        "https://www.srca.nm.gov/parts/title08/08.015.0002.html",
        "https://www.law.cornell.edu/cfr/text/45/98.45",
    )

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.nm.ececd.ccap.copay.schedule
        ratio = spm_unit("nm_ccap_income_to_fpg_ratio", period)
        countable_income = spm_unit("nm_ccap_countable_income", period)
        # 8.15.2.24: the first child in care is charged the full sliding-scale
        # share of monthly countable income; each additional child in care is
        # charged additional_child_share of that amount.
        first_child_copay = countable_income * p.rate.calc(ratio)
        person = spm_unit.members
        eligible_child = person("nm_ccap_eligible_child", period)
        # "In care" is narrower than "age eligible": a family with two children
        # under 13 but only one in paid care is charged for one child. Care
        # receipt is tracked by childcare hours, which nm_ccap_service_unit
        # already reads for the part-time rate fractions.
        in_care = person("childcare_hours_per_week", period.this_year) > 0
        children_in_care = spm_unit.sum(eligible_child & in_care)
        additional_children = max_(children_in_care - 1, 0)
        total = first_child_copay * (1 + additional_children * p.additional_child_share)
        # The floor is inclusive: a family exactly at 200% FPG pays nothing.
        # The rate brackets alone would not give that, because the bracket
        # starting at 2 applies AT 2, so the floor is tested separately.
        above_floor = ratio > p.fpl_floor
        return where(above_floor & (children_in_care > 0), total, 0)
