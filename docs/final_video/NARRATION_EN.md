# Five-minute English narration

Read at approximately 125–140 words per minute. Chapter timings are editing targets; align subtitle timing to the final recording.

The generated preview is silent. Record this narration separately.

## 00:00:00–00:00:15 | Beyond a successful grasp

Our project studies autonomous robot manipulation beyond a successful grasp. Using a Franka Panda in MuJoCo, we ask where a complete pick-and-place pipeline breaks, and which targeted changes recover the task.

*31 words; target 124 words/minute.*

## 00:00:15–00:00:40 | A complete physical baseline

The baseline loads six public YCB models and supports seeded random object selection and placement. The robot proposes grasps, checks motion, closes its fingers, lifts, transports and physically releases the object. We evaluate repeated randomized trials and retain failures. The object moves through simulated contact dynamics, without a robot-object weld or teleportation.

*52 words; target 125 words/minute.*

## 00:00:40–00:01:10 | Verify the whole task

Our modules separate observation, candidate generation, inverse kinematics, collision checking and execution. Success requires an eighty-millimeter lift, one-second hold, sustained bilateral contact, stable release and placement within fifty-five millimeters. Clutter tests also limit neighbor displacement. Some observers use measured points, but planning still uses simulator geometry. This is a controlled simulation study, rather than an end-to-end real-camera system.

*58 words; target 116 words/minute.*

## 00:01:10–00:01:40 | RQ1: escape a blocked approach

First, a nearby can blocks the robot's palm. The original candidates are safely rejected before motion. In the same scene, we append a bounded family of inclined and offset grasps while preserving all collision checks. The new candidate completes the transfer. This development example illustrates the mechanism; the separate paired experiment measures how often it helps.

*56 words; target 112 words/minute.*

## 00:01:40–00:02:25 | RQ3: retention versus deformation

Next, we replace the rigid target with a genuine three-dimensional elastic solid. The controller measures normal force at both fingers and adjusts bounded preload using the weaker contact. Fixed preload completes two of six soft-object tasks; force regulation completes six of six. Under randomized rigid-object mass, friction and actuator delay, completion changes from ten of twelve to twelve of twelve. However, average peak elastic strain increases from about three-point-seven to four-point-nine percent. The result supports retention within the tested limits, not reduced deformation. The force and strain curves shown here are from an illustrative development run.

*96 words; target 128 words/minute.*

## 00:02:25–00:03:05 | RQ2: more frames can be worse

More observations do not automatically improve manipulation. We add missing stripes, drift, outliers and calibration bias to synthetic depth. A single packet completes six of twelve tasks, while raw twenty-four-packet fusion completes only one: accumulated outliers can distort foreground geometry. Requiring each voxel to receive support from three different packets raises completion to nine of twelve. All remaining failures are wedge-shaped objects losing contact. The bottleneck moves from obtaining usable geometry toward retaining the object, although shape and estimation effects are not separately isolated.

*84 words; target 126 words/minute.*

## 00:03:05–00:03:40 | Detect, withdraw, reobserve, retry

For recovery, we inject a transient closure fault: the first commanded opening remains wider than the target. Missing bilateral contact triggers a real grasp failure. The robot opens, performs a checked withdrawal, reobserves and physically grasps again. The scene is initialized once and never reset between attempts. All six first attempts fail, and all six retry episodes succeed. This verifies recovery from the specified temporary fault, rather than a universal recovery rate for natural failures.

*75 words; target 129 words/minute.*

## 00:03:40–00:04:05 | Additional directions, honest boundaries

Additional studies carry a freely hinged assembly and estimate grasps for procedural objects without supplying target CAD. The shape methods tie at eleven of twelve. In stronger clutter, active observation actually falls from five of six to three of six because of additional placement failures. We keep these unfavorable results instead of presenting every extension as an improvement.

*58 words; target 139 words/minute.*

## 00:04:05–00:04:40 | Paired evidence, not selected successes

The candidate study contains one hundred eighty physical episodes. Local alternatives change completion from fifty-four to fifty-eight out of sixty with three neighbors, and from twenty-six to twenty-nine out of thirty with five. The exploratory study separately contains one hundred twenty-six episodes. We pair initial scenes and physics, preserve failures and report confidence intervals. No comparison passes its stated statistical threshold. Development footage is excluded from these denominators, and the two studies are never pooled into one success rate.

*79 words; target 135 words/minute.*

## 00:04:40–00:05:00 | What the experiments teach us

Our main finding is that geometry, observation quality and contact retention must be evaluated together. The deliverables include runnable source, frozen records, a ten-page report and reproduction instructions. Forty-nine tests and both evidence audits pass. Future work targets wedge stability, deformation-aware control and less ideal sensing.

*46 words; target 138 words/minute.*

**Total: 635 words in 300 seconds (127.0 words/minute).**
