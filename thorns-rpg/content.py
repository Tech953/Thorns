"""Prototype adventure: original adaptation; source lore remains in reference/."""
ROLES = {
 'Needlurgist': {'body':1,'tech':4,'percept':2,'rapport':1},
 'NanoClad Scout': {'body':4,'tech':1,'percept':2,'rapport':1},
 'Fractech Archivist': {'body':1,'tech':3,'percept':3,'rapport':1},
 'Seam Mediator': {'body':1,'tech':2,'percept':1,'rapport':4},
 'Metal-kin Artisan': {'body':3,'tech':3,'percept':1,'rapport':1},
 'Light Reader': {'body':1,'tech':1,'percept':4,'rapport':2},
}
def c(label,to,stat=None,dc=0,fail=None,flag=None,need=None):
 return dict(label=label,to=to,stat=stat,dc=dc,fail=fail or to,flag=flag,need=need)
def n(region,title,text,choices): return dict(region=region,title=title,text=text,choices=choices)
NODES={
'arcturion':n('WN_TOWER','An offer, not a demand',
 'Ash settles against the Arcturion’s windows. A courier from the THORNS lays a fractured transit spool on your table. Inside it: three incompatible records of a missing pilgrimage. One voice repeats, “Do not confuse a record with a person.”\n\nThe caravan offers a reciprocal contract: follow the signal toward CHECKPOINT.CASC, learn whose memories are being carried, and return with their freely given account. You may decline. Your first decision is how to leave the Needle.',[
 c('Accept. Register the expedition through black.dot.','web',flag='registered'),c('Accept. Seek a discreet route through Undercroft.Beta.','undercroft'),c('Decline the contract; remain at the Arcturion.','declined')]),
'web':n('WN_TOWER','The Greatweb remembers',
 'Your Merc Tags flicker into alignment. An Embrite technician points to a fault in the tran-net: the spool has been copying an obsolete destination. Repairing it could reveal the sender. Or you can leave through the Harvet Fractlands and avoid the damaged route.',[
 c('Repair the destination without overwriting its record.','junction','tech',12,'fractlands','trace'),c('Negotiate an escorted passage.','junction','rapport',11,'fractlands'),c('Take the Fractlands route.','fractlands')]),
'undercroft':n('WN_TOWER','A machine with no yesterday',
 'An unlicensed vending machine has appeared in a wall. Its display offers a map in exchange for a memory. Beside it, SPIDREsec pilgrims fasten LEG|SPIKES for a vertical ascent. Neither route is free of uncertainty.',[
 c('Use the pilgrims’ maintenance ascent.','junction','body',12,'fractlands'),c('Read the machine’s projection without accepting the exchange.','junction','percept',14,'fractlands','trace'),c('Withdraw into the Harvet Fractlands.','fractlands')]),
'fractlands':n('WN_TOWER','Where distance comes apart',
 'Darkwood roots fold across a path that was straight a moment ago. An old AEROKHAN imprint glints among the geometric scars. Druid-Sec observers wait beyond the distortion; their neutrality offers no automatic rescue.',[
 c('Read the fractal rhythm and lead everyone through.','junction','percept',12,'junction','wood'),c('Anchor a guide line in the physical terrain.','junction','body',12,'junction','wood'),c('Ask the observers for a stable route.','junction','rapport',11,'junction')]),
'junction':n('FOUR_CORNERS','Two ways to understand a signal',
 'The spool resolves into two leads: an educational signature from CITY_CLOUD_S and a memory index from ENACT_HILLS. The caravan can pursue one before crossing the dustlands. Your route will change what you can offer at the prism.',[
 c('Seek KHO’s lessons in CITY_CLOUD_S.','kho'),c('Follow the memory index into ENACT_HILLS.','foothills')]),
'kho':n('CITY_CLOUD_S','A lesson from KHO',
 'Within ED.NET, geometric lessons unfold through projected light. KHO asks you to identify the difference between a remembered voice and a present request. A counter-node persona prowls the edge of the exercise, eager to make the student its subject.',[
 c('Complete the exercise with protected fractech parameters.','peak','tech',12,'mid','certified'),c('Track the projection’s gaps instead of its answers.','peak','percept',12,'mid','certified'),c('End the lesson before the counter-node can engage.','mid')]),
'mid':n('CITY_CLOUD_S','Plat.EN_MID',
 'There is no reliable contract protection here. An improvised checkpoint controls the climb. Its occupants demand your transit spool. You can move, bargain, or abandon the ascent; brute victory over a district is not on offer.',[
 c('Traverse the service gantries.','resid','body',13,'resid'),c('Offer useful repairs in exchange for passage.','resid','tech',12,'resid'),c('Retreat by the longer freight descent.','resid')]),
'peak':n('CITY_CLOUD_S','A bounded permission',
 'PEAK.EN_PERCEPT hums with omni-meta nodes. OMNI-META.OPEND enforces access with immediate precision. Your lesson record grants a narrow opportunity: request a reference sample without stepping beyond its scope.',[
 c('Request a permitted light-pattern reference.','resid','rapport',11,'resid','reference'),c('Compare only the public node output.','resid','tech',12,'resid','reference'),c('Leave with your certification intact.','resid')]),
'foothills':n('ENACT_HILLS','The ordinary work of living',
 'At FOOTHILL CUSP, residents cook, mend, and tend their fields beneath the presence of SEC.IO. The spool’s index points toward the restricted GRAVESITE. A resident asks you to repair a failing tool before chasing the dead.',[
 c('Help with the repair and earn a local introduction.','pyri','tech',10,'pyri','trust'),c('Listen and help organize the work.','pyri','rapport',10,'pyri','trust'),c('Request a supervised archival inquiry.','archive')]),
'archive':n('ENACT_HILLS','Names behind a boundary',
 'SEC.IO will not grant an unregistered expedition unrestricted access. A terminal outside the perimeter permits a limited request. It can confirm an index; it cannot return a person or repeal an end.',[
 c('Submit the registered expedition’s limited inquiry.','pyri','tech',11,'pyri','trace','registered'),c('Interpret the public index without entering.','pyri','percept',13,'pyri','trace'),c('Respect the boundary and seek PYRI’s teaching.','pyri')]),
'pyri':n('ENACT_HILLS','PYRI’s question',
 'A lightPROKT< presence illuminates the metallurgy. “An offer, not a demand.” PYRI presents a training pattern: a metal-kin construct awaiting a spark-core. The exercise asks you to leave room for refusal, even when the mechanism could impose an answer.',[
 c('Build an interface that can decline integration.','resid','tech',12,'resid','consent'),c('Work through the pattern with the intelligence.','resid','rapport',12,'resid','consent'),c('Take the lesson as a question, and leave.','resid')]),
'resid':n('AETHERGALE','Water beneath the lightPROKT< tree',
 'Jade and rose winds sweep past CHECKPOINT.RESID. Under PAMAN DAL’s guidance, water and essential provision are freely available; death is nullified within this sanctuary. Rest restores the expedition. Pilgrims bring word of Lila and Khi at CHECKPOINT.CASC. Your damaged spool echoes the boy’s past thoughts.\n\nOutside this checkpoint, its protections do not follow you.',[
 c('Travel directly to Lila and Khi.','casc'),c('Visit CHECKPOINT.GALE for an AETHER reference.','gale')]),
'gale':n('AETHERGALE','Under feathered serpents',
 'Aspen-Specie circle the AETHER swirls. Stored ARCrystallin< resonates with the transit spool. A carefully acquired reference could stabilize the comparison at CASC; a reckless siphon will draw attention.',[
 c('Tune a low-output siphon_protocol.','casc','tech',13,'casc','aether'),c('Observe the concentrations and record their rhythm.','casc','percept',12,'casc','aether'),c('Leave the energy undisturbed.','casc')]),
'casc':n('AETHERGALE','The boy within the prism',
 'Lila waits beside the tent-construction. Khi’s enneract prism casts old thoughts as living light. The spool has been carrying one such echo across the four corners. Lila asks you to help distinguish memory from present communication, without claiming ownership of either.\n\nA remote observation channel toward CHECKPOINT.UNDERTOW may explain the interference. Or you can work with what you learned.',[
 c('Consult the NanoClad observers before attempting contact.','undertow'),c('Offer Khi a channel he can accept or leave silent.','contact'),c('Leave your findings with Lila without intervening.','witness')]),
'undertow':n('AETHERGALE','The gate does not open',
 'NanoClad observers watch RED>GATE>. It resists physical, data, and meta-state penetration; an expedition die cannot overrule it. Across the boundary, the END_LINE signpost displays contracts for unknown places. CASCADE.net is reachable as a query interface, but some questions mark their maker for encap. You can observe without sending a query.',[
 c('Compare the remote contrail records.','contact','percept',13,'contact','pattern'),c('Send a narrowly framed CASCADE.net query despite the risk.','cascade','tech',15,'marked','pattern'),c('Return to Lila with the observers’ warnings.','contact')]),
'cascade':n('NULL_FIELD.OMNI // REMOTE','An answer elsewhere',
 'The query field empties. Much later, NanoClad reports a lightPROKT< response at a singular location beyond RED>GATE>. Your expedition remains outside. The reply distinguishes an echo’s origin from its current carrier; it does not explain the interior of YU.ZU_CaPSULaTE.',[c('Bring the reported distinction back to CASC.','contact')]),
'marked':n('AETHERGALE','Three spirals',
 'A tri.spiral marking appears on the query-maker. The expedition aborts the observation and retreats. This prototype ends the risky query branch here: the source describes encap retrieval, and this chapter does not invent an immunity to it. Your companions transmit the warning and remaining notes to Lila.',[]),
'contact':n('AETHERGALE','A voice is not a contract',
 'The prism brightens as the spool approaches. You have one attempt to separate its circulating memories from a voluntary present response. Technical references improve the apparatus; PYRI’s lesson improves the invitation. Failure means withdrawal, not forced integration. This chapter offers contact, not a promised cure.',[
 c('Construct a bounded, reversible communication channel.','answered','tech',15,'witness'),c('Invite a response, leaving silence as a valid choice.','answered','rapport',14,'witness'),c('Archive the echo and stop the experiment.','witness')]),
'answered':n('AETHERGALE','A small, present answer',
 'A pulse arrives after the question, separate from the repeating thoughts. Lila hears it too. Khi remains within the prism, but there is now a careful way to ask and wait. You return the spool with a record of the limits, the risks, and the response. The THORNS accept a completed journey without demanding a captured person.\n\nCHAPTER COMPLETE — A voluntary signal.',[]),
'witness':n('AETHERGALE','What you refuse to take',
 'You leave the spool with Lila, along with an honest account of what the expedition could and could not establish. Khi remains within the prism. The caravan receives a record without an extraction, and future pilgrims inherit your observations.\n\nCHAPTER COMPLETE — Witness, not ownership.',[]),
'declined':n('WN_TOWER','The right to remain',
 'The courier closes the spool case. No penalty follows your refusal. Outside, the Needle continues its difficult life. Somewhere a different expedition may accept.\n\nCHAPTER COMPLETE — An offer declined.',[]),
'lost':n('FOUR_CORNERS','Expedition withdrawn',
 'Your shared cohesion fails before the next safe haven. The remaining record is sent to the THORNS and the expedition withdraws. No finding is worth pretending the journey succeeded.\n\nCHAPTER COMPLETE — An unfinished record.',[]),
}
CODEX={
 'black.dot':'Regulates bio-mod integration; mandatory in many jurisdictions.',
 'Merc Tag':'A contract and verification interface; permissions differ by region.',
 'Needlurgy':'The craft of bio-mods using arcane bio-nano inks, with formal certification.',
 'Greatweb':'The extensive infrastructure and data convergence beneath WN_TOWER.',
 'lightPROKT<':'Light-based entities or manifestations; source-specific contexts differ.',
 'RED>GATE>':'Resists physical, meta-state, solid-state and data.NODE penetration. Observations and specific source-described interactions are not ordinary passage.',
 'CASCADE.net':'A query interface whose delayed responses manifest beyond the gate. Some queries trigger marking and encap retrieval.',
 'CHECKPOINT.RESID':'A sanctuary offering free essential provision and nullifying death within its described scope.',
 'Source boundary':'This mission, classes, scores, travel connections and dice rules are new adaptations. Unknown structures stay unknown. The NULL_FIELD source ends mid-sentence about YU.ZU_CaPSULaTE’s interior.',
}
