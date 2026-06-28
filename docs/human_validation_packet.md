# Human Validation Packet

This packet prepares the 20-scene human validation proposed in `additional_experiments_gpt55_plan.md`. It contains no collected human annotations, so it is a protocol artifact rather than a validation result.

## Files

- Participant-safe items: `data/human_validation_items.jsonl`
- Response template: `data/human_validation_response_template.csv`
- Static annotation page: `docs/human_validation_packet.html`
- Researcher-only answer key: `results/human_validation_answer_key.json`

## Summary

Items: 20. Condition counts: mirror_success_control=5, partial_mirror_failure=5, perspective_mirror_failure=10.

Participant files exclude condition labels, scene IDs, target IDs, and held-out success rates. The answer key keeps those fields for analysis after annotation.

## Annotation Instructions

For each item, annotators see a referring message and listener-visible object options. They should choose the object the message refers to and mark whether the message is ambiguous from the visible information.

Recommended collection: three independent annotations per item. Report accuracy and ambiguity rate by condition only after annotations are collected.

## Item Preview

| Item | Message | Options |
|---|---|---|
| HVAL_001 | It’s a large red sphere. | obj_1: large red sphere at row 4, column 1<br>obj_5: large blue sphere at row 2, column 3<br>obj_2: large red sphere at row 1, column 4<br>obj_3: large green cylinder at row 4, column 2<br>obj_4: small orange cylinder at row 5, column 5 |
| HVAL_002 | Find the small yellow sphere left of the large green cube. | obj_5: small green cube at row 2, column 3<br>obj_2: small yellow sphere at row 1, column 4<br>obj_1: small yellow sphere at row 4, column 1<br>obj_3: large green cube at row 4, column 2<br>obj_4: small orange pyramid at row 5, column 5 |
| HVAL_003 | It’s a large red sphere. | obj_1: large red sphere at row 4, column 1<br>obj_5: large green cylinder at row 2, column 3<br>obj_3: large orange cube at row 4, column 2<br>obj_2: large red sphere at row 1, column 4<br>obj_4: large blue sphere at row 5, column 5 |
| HVAL_004 | It’s a small green sphere. | obj_1: small green sphere at row 4, column 1<br>obj_5: large red cube at row 2, column 3<br>obj_4: large purple cylinder at row 5, column 5<br>obj_2: small green sphere at row 1, column 4<br>obj_3: large red cylinder at row 4, column 2 |
| HVAL_005 | It’s a small blue cube. | obj_1: small blue cube at row 4, column 1<br>obj_4: small orange cylinder at row 5, column 5<br>obj_2: small blue cube at row 1, column 4<br>obj_3: large yellow pyramid at row 4, column 2<br>obj_5: large green cone at row 2, column 3 |
| HVAL_006 | Large blue cube. | obj_3: large purple pyramid at row 4, column 2<br>obj_1: large blue cube at row 4, column 1<br>obj_4: large red cube at row 5, column 5<br>obj_5: small purple sphere at row 2, column 3<br>obj_2: large blue cube at row 1, column 4 |
| HVAL_007 | Find the large yellow cube left of the purple cylinder. | obj_4: large purple pyramid at row 5, column 5<br>obj_2: large yellow cube at row 1, column 4<br>obj_1: large yellow cube at row 4, column 1<br>obj_5: small yellow cone at row 2, column 3<br>obj_3: large purple cylinder at row 4, column 2 |
| HVAL_008 | It’s a small blue sphere. | obj_5: small blue cube at row 2, column 3<br>obj_4: small red pyramid at row 5, column 5<br>obj_3: large red cone at row 4, column 2<br>obj_1: small blue sphere at row 4, column 1<br>obj_2: small blue sphere at row 1, column 4 |
| HVAL_009 | It’s a large yellow cube. | obj_1: large yellow cube at row 4, column 1<br>obj_2: large yellow cube at row 1, column 4<br>obj_4: large purple sphere at row 5, column 5<br>obj_5: small green sphere at row 2, column 3<br>obj_3: large green sphere at row 4, column 2 |
| HVAL_010 | Small red sphere. | obj_3: large yellow cylinder at row 4, column 2<br>obj_1: small red sphere at row 4, column 1<br>obj_4: large orange sphere at row 5, column 5<br>obj_5: small blue cylinder at row 2, column 3<br>obj_2: small red sphere at row 1, column 4 |
| HVAL_011 | Large red sphere. | obj_1: large red sphere at row 3, column 2<br>obj_2: large red sphere at row 3, column 4<br>obj_4: large purple pyramid at row 4, column 2<br>obj_5: small blue sphere at row 5, column 5 |
| HVAL_012 | Large red sphere. | obj_1: large red sphere at row 3, column 2<br>obj_2: large red sphere at row 3, column 4<br>obj_4: large green cylinder at row 4, column 2<br>obj_5: large purple pyramid at row 5, column 5 |
| HVAL_013 | Small green sphere. | obj_1: small green sphere at row 3, column 2<br>obj_5: large red cube at row 5, column 5<br>obj_4: large purple cone at row 4, column 2<br>obj_2: small green sphere at row 3, column 4 |
| HVAL_014 | Large yellow sphere. | obj_1: large yellow sphere at row 3, column 2<br>obj_5: small purple pyramid at row 5, column 5<br>obj_2: large yellow sphere at row 3, column 4<br>obj_4: large green pyramid at row 4, column 2 |
| HVAL_015 | Small blue cube. | obj_1: small blue cube at row 3, column 2<br>obj_4: large purple sphere at row 4, column 2<br>obj_2: small blue cube at row 3, column 4<br>obj_5: large green cone at row 5, column 5 |
| HVAL_016 | Go to row 4, column 1: small blue cube. | obj_5: large red cube at row 2, column 3<br>obj_2: small blue cube at row 1, column 4<br>obj_1: small blue cube at row 4, column 1<br>obj_3: large red sphere at row 4, column 2<br>obj_4: large yellow cylinder at row 5, column 5 |
| HVAL_017 | It’s a large blue sphere. | obj_5: small blue cylinder at row 2, column 3<br>obj_1: large blue sphere at row 4, column 1<br>obj_2: large blue sphere at row 1, column 4<br>obj_4: large purple cube at row 5, column 5<br>obj_3: large green pyramid at row 4, column 2 |
| HVAL_018 | It’s the leftmost large yellow sphere, below the top row. | obj_2: large yellow sphere at row 1, column 4<br>obj_5: large yellow sphere at row 2, column 3<br>obj_3: large red cone at row 4, column 2<br>obj_1: large yellow sphere at row 4, column 1<br>obj_4: small blue pyramid at row 5, column 5 |
| HVAL_019 | Go to row 4, column 1: the large blue sphere. | obj_3: large purple cone at row 4, column 2<br>obj_2: large blue sphere at row 1, column 4<br>obj_1: large blue sphere at row 4, column 1<br>obj_4: small orange sphere at row 5, column 5<br>obj_5: small yellow cube at row 2, column 3 |
| HVAL_020 | It’s a small blue sphere. | obj_3: large red pyramid at row 4, column 2<br>obj_5: large green cube at row 2, column 3<br>obj_1: small blue sphere at row 4, column 1<br>obj_2: small blue sphere at row 1, column 4<br>obj_4: small blue cube at row 5, column 5 |
