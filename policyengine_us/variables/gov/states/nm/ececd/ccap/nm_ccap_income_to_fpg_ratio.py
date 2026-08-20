from policyengine_us.model_api import *


class nm_ccap_income_to_fpg_ratio(Variable):
    value_type = float
    entity = SPMUnit
    label = (
        "New Mexico CCAP countable income as a share of the federal poverty guideline"
    )
    definition_period = MONTH
    unit = "/1"
    defined_for = StateCode.NM
    reference = "https://www.srca.nm.gov/parts/title08/08.015.0002.html"

    def formula(spm_unit, period, parameters):
        # Both sides are monthly: nm_ccap_countable_income is a MONTH variable
        # and spm_unit_fpg is annual, so reading it with the bare MONTH period
        # auto-divides it to a monthly amount -- the same pattern
        # nm_ccap_income_eligible uses for its FPL ceilings.
        countable_income = spm_unit("nm_ccap_countable_income", period)
        fpg = spm_unit("spm_unit_fpg", period)
        # New Mexico is always in the CONTIGUOUS_US state group, so the
        # guideline is strictly positive and the division is safe. A family with
        # a business loss can have negative countable income and therefore a
        # negative ratio; that lands below the copayment floor, which is the
        # intended result.
        return countable_income / fpg
