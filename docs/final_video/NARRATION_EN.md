# Five-minute English narration — picture-aligned revision

Read each timed cue within its allotted interval. Times were assigned to the reviewed pictures, not estimated from chapter word counts.

The generated preview is silent. Record this narration separately.

## 00:00:00–00:00:15 | Beyond a successful grasp

Our project studies complete physical pick-and-place with a Franka Panda in MuJoCo. We investigate blocked approaches, corrupted geometry and contact retention. The aim is to explain task failures and test bounded interventions.

*32 words; target 128 words/minute.*

| Time | Read this cue |
|---|---|
| 00:00:00–00:00:06 | Our project studies complete physical pick-and-place with a Franka Panda in MuJoCo. |
| 00:00:06–00:00:10 | We investigate blocked approaches, corrupted geometry and contact retention. |
| 00:00:10–00:00:15 | The aim is to explain task failures and test bounded interventions. |

## 00:00:15–00:00:45 | A complete physical baseline

The baseline loads six public YCB models and supports seeded random object selection and placement. This complete run starts with a checked approach and physical finger closure. Contact lifts and holds the target before the robot begins its transfer. The arm carries the object to the destination, lowers it and opens the fingers. Release and table support are checked; failures remain in the evaluation.

*64 words; target 128 words/minute.*

| Time | Read this cue |
|---|---|
| 00:00:15–00:00:24 | The baseline loads six public YCB models and supports seeded random object selection and placement. |
| 00:00:24–00:00:30 | This complete run starts with a checked approach and physical finger closure. |
| 00:00:30–00:00:35 | Contact lifts and holds the target before the robot begins its transfer. |
| 00:00:35–00:00:41 | The arm carries the object to the destination, lowers it and opens the fingers. |
| 00:00:41–00:00:45 | Release and table support are checked; failures remain in the evaluation. |

## 00:00:45–00:01:10 | Verify the whole task

Mesh-based candidates are proposals. Inverse kinematics and collision checks decide which can execute. Complete success requires an eighty-millimeter lift, a one-second hold and sustained bilateral contact. Release must be stable, within fifty-five millimeters of the destination. Planning still uses simulator geometry; sensing is synthetic.

*44 words; target 106 words/minute.*

| Time | Read this cue |
|---|---|
| 00:00:45–00:00:55 | Mesh-based candidates are proposals. Inverse kinematics and collision checks decide which can execute. |
| 00:00:55–00:01:02 | Complete success requires an eighty-millimeter lift, a one-second hold and sustained bilateral contact. |
| 00:01:02–00:01:06 | Release must be stable, within fifty-five millimeters of the destination. |
| 00:01:06–00:01:10 | Planning still uses simulator geometry; sensing is synthetic. |

## 00:01:10–00:01:40 | RQ1: escape a blocked approach

The original candidates are rejected because a nearby can blocks the palm. We keep the scene and safety checks, adding bounded inclined and offset grasp alternatives. The chosen alternative lifts the target and carries it through the checked corridor. The robot lowers and releases it. This development demonstration is separate from the paired evaluation.

*54 words; target 108 words/minute.*

| Time | Read this cue |
|---|---|
| 00:01:10–00:01:15 | The original candidates are rejected because a nearby can blocks the palm. |
| 00:01:15–00:01:24 | We keep the scene and safety checks, adding bounded inclined and offset grasp alternatives. |
| 00:01:24–00:01:33 | The chosen alternative lifts the target and carries it through the checked corridor. |
| 00:01:33–00:01:40 | The robot lowers and releases it. This development demonstration is separate from the paired evaluation. |

## 00:01:40–00:02:25 | RQ3: retention versus deformation

This elastic model genuinely deforms; the YCB foam brick in the baseline remains rigid. The controller regulates the weaker finger contact to retain the object during lift and transfer. Fixed preload completes two of six soft-object tasks; regulation completes six of six. These force and strain curves illustrate one development run, rather than a group average. Across formal trials, mean peak strain rises from about three-point-seven to four-point-nine percent. Retention improves within the tested limits; reduced deformation is not demonstrated. A separate rigid-load study randomizes mass, friction and actuator delay. Regulation changes completion from ten of twelve to twelve of twelve.

*101 words; target 135 words/minute.*

| Time | Read this cue |
|---|---|
| 00:01:40–00:01:46 | This elastic model genuinely deforms; the YCB foam brick in the baseline remains rigid. |
| 00:01:46–00:01:54 | The controller regulates the weaker finger contact to retain the object during lift and transfer. |
| 00:01:54–00:02:01 | Fixed preload completes two of six soft-object tasks; regulation completes six of six. |
| 00:02:01–00:02:07 | These force and strain curves illustrate one development run, rather than a group average. |
| 00:02:07–00:02:11 | Across formal trials, mean peak strain rises from about three-point-seven to four-point-nine percent. |
| 00:02:11–00:02:15 | Retention improves within the tested limits; reduced deformation is not demonstrated. |
| 00:02:15–00:02:20 | A separate rigid-load study randomizes mass, friction and actuator delay. |
| 00:02:20–00:02:25 | Regulation changes completion from ten of twelve to twelve of twelve. |

## 00:02:25–00:03:05 | RQ2: more frames can be worse

Synthetic depth includes missing stripes, drift, outliers and a persistent calibration bias. The single-packet method completes six of twelve tasks; naive fusion completes only one. Cross-packet voxel support rejects transient outliers and reaches nine successes in twelve trials. This successful development example uses the robust observer, without target CAD or instance labels in grasp estimation. Planning still uses simulator geometry; measured observations do not make the entire system vision-only. The robot carries and releases the object in this illustration. The formal failures remain wedge slips, in separate trials.

*88 words; target 132 words/minute.*

| Time | Read this cue |
|---|---|
| 00:02:25–00:02:30 | Synthetic depth includes missing stripes, drift, outliers and a persistent calibration bias. |
| 00:02:30–00:02:35 | The single-packet method completes six of twelve tasks; naive fusion completes only one. |
| 00:02:35–00:02:40 | Cross-packet voxel support rejects transient outliers and reaches nine successes in twelve trials. |
| 00:02:40–00:02:49 | This successful development example uses the robust observer, without target CAD or instance labels in grasp estimation. |
| 00:02:49–00:02:56 | Planning still uses simulator geometry; measured observations do not make the entire system vision-only. |
| 00:02:56–00:03:01 | The robot carries and releases the object in this illustration. |
| 00:03:01–00:03:05 | The formal failures remain wedge slips, in separate trials. |

## 00:03:05–00:03:40 | Detect, withdraw, reobserve, retry

A transient command fault leaves the first closure wider than the target. No bilateral contact is detected; the grasp is rejected. The robot opens and withdraws safely. It reobserves and makes a second grasp in the same evolving scene. The second grasp holds through lift and transfer; the scene was never reset. After lowering and release, table support and final placement are verified. All six controlled episodes recover; broader recovery remains unproven.

*72 words; target 123 words/minute.*

| Time | Read this cue |
|---|---|
| 00:03:05–00:03:10 | A transient command fault leaves the first closure wider than the target. |
| 00:03:10–00:03:13.5 | No bilateral contact is detected; the grasp is rejected. |
| 00:03:13.5–00:03:16 | The robot opens and withdraws safely. |
| 00:03:16–00:03:21 | It reobserves and makes a second grasp in the same evolving scene. |
| 00:03:21–00:03:29 | The second grasp holds through lift and transfer; the scene was never reset. |
| 00:03:29–00:03:36 | After lowering and release, table support and final placement are verified. |
| 00:03:36–00:03:40 | All six controlled episodes recover; broader recovery remains unproven. |

## 00:03:40–00:04:05 | Additional directions, honest boundaries

A passive hinge remains dynamic while the whole assembly is transported. All six assembly tasks succeed; deliberate lid opening is not demonstrated. Measured points propose grasps for procedural instances without target CAD. Both methods tie at eleven of twelve, with one shared slip. In separate stronger-clutter trials, active sensing changes completion from five of six to three of six.

*59 words; target 142 words/minute.*

| Time | Read this cue |
|---|---|
| 00:03:40–00:03:45 | A passive hinge remains dynamic while the whole assembly is transported. |
| 00:03:45–00:03:50 | All six assembly tasks succeed; deliberate lid opening is not demonstrated. |
| 00:03:50–00:03:54 | Measured points propose grasps for procedural instances without target CAD. |
| 00:03:54–00:03:58 | Both methods tie at eleven of twelve, with one shared slip. |
| 00:03:58–00:04:05 | In separate stronger-clutter trials, active sensing changes completion from five of six to three of six. |

## 00:04:05–00:04:40 | Paired evidence, not selected successes

The candidate study contains one hundred eighty paired physical episodes. With three neighbors, local alternatives change success from fifty-four to fifty-eight out of sixty. With five neighbors, success changes from twenty-six to twenty-nine out of thirty. The separate exploratory screening contains one hundred twenty-six episodes across fourteen conditions. The intervals show substantial uncertainty; none of the comparisons passes its stated statistical threshold. Initial scenes and physics are paired, with all failures retained. Development demonstrations are excluded from both evaluation denominators.

*80 words; target 137 words/minute.*

| Time | Read this cue |
|---|---|
| 00:04:05–00:04:10 | The candidate study contains one hundred eighty paired physical episodes. |
| 00:04:10–00:04:16 | With three neighbors, local alternatives change success from fifty-four to fifty-eight out of sixty. |
| 00:04:16–00:04:23 | With five neighbors, success changes from twenty-six to twenty-nine out of thirty. |
| 00:04:23–00:04:28 | The separate exploratory screening contains one hundred twenty-six episodes across fourteen conditions. |
| 00:04:28–00:04:33 | The intervals show substantial uncertainty; none of the comparisons passes its stated statistical threshold. |
| 00:04:33–00:04:37 | Initial scenes and physics are paired, with all failures retained. |
| 00:04:37–00:04:40 | Development demonstrations are excluded from both evaluation denominators. |

## 00:04:40–00:05:00 | What the experiments teach us

The main finding is to diagnose geometry, sensing and contact retention together. Source code, frozen records and the ten-page report provide reproduction instructions. Forty-nine tests and both evidence audits pass. Next steps target wedge stability, deformation-aware control and less ideal sensing.

*41 words; target 123 words/minute.*

| Time | Read this cue |
|---|---|
| 00:04:40–00:04:46 | The main finding is to diagnose geometry, sensing and contact retention together. |
| 00:04:46–00:04:52 | Source code, frozen records and the ten-page report provide reproduction instructions. |
| 00:04:52–00:04:56 | Forty-nine tests and both evidence audits pass. |
| 00:04:56–00:05:00 | Next steps target wedge stability, deformation-aware control and less ideal sensing. |

**Total: 635 words in 300 seconds (127.0 words/minute).**
