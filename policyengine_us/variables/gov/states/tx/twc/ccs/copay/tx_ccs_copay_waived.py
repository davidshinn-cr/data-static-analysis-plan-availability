from policyengine_us.model_api import *


class tx_ccs_copay_waived(Variable):
    value_type = bool
    entity = SPMUnit
    definition_period = MONTH
    label = "Texas CCS Parent Share of Cost waived"
    defined_for = StateCode.TX
    reference = (
        "https://www.law.cornell.edu/regulations/texas/40-Tex-Admin-Code-SS-809-19"
    )

    def formula(spm_unit, period, parameters):
        p = parameters(period).gov.states.tx.twc.ccs.copay.waiver
        # 40 TAC 809.19(d) lists the families a Board may not assess a Parent
        # Share of Cost against. Each branch is gated by its own parameter so a
        # Board policy change can be encoded without touching this formula.
        protective_services = spm_unit("receives_tx_ccs_protective_services", period)
        tanf = spm_unit("is_tanf_enrolled", period)
        return (protective_services & p.protective_services) | (
            tanf & p.tanf_or_choices
        )
