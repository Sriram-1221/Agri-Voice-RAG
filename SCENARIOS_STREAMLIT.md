# Agricultural FAQ RAG System - Test Scenarios

This document contains realistic test scenarios based on the actual FAQ content to validate system accuracy, intent detection, and performance.

## Scenario Classification

### 1A: Agriculture with Context (40 scenarios)
Questions about topics **actually covered** in the FAQ document that should return specific, accurate answers.

### 1B: Agriculture without Context (15 scenarios) 
Agricultural questions **NOT covered** in the FAQ document that should return: "I don't know. I can help you by transferring the call to subject matter expertise if needed."

### 2: Non-Agriculture (15 scenarios)
Non-agricultural questions that should return: "I can answer only agriculture related queries."

---

## Scenario 1A: Agriculture with Context (40 scenarios)
*These are based on actual FAQ content and should return accurate, grounded answers*

1. What is Dormulin Vegetative used for?
2. What is Dormulin Flowering designed for?
3. What is the fertilizer ratio for banana rooting stage?
4. What are the benefits of Zetol Select for banana vegetative stage?
5. What is the dosage of Trail Blaze for chilli seeds?
6. How much Actin Granules should be applied per acre for chilli?
7. What is the dosage of Tracs Sure for chilli?
8. What is the foliar spray dosage of Zetol Select for chilli?
9. What is the dosage of Akre Shield for chilli?
10. How to control damping-off in chilli?
11. How to control bacterial leaf spot in chilli?
12. How to control powdery mildew in chilli?
13. How to control thrips and mites in chilli?
14. How to control whiteflies in chilli?
15. How to control fruit borer in chilli?
16. What is the seed treatment dosage for Trail Blaze in tomato?
17. How much Actin Granules for tomato per acre?
18. How to control potash deficiency in tomato?
19. How to control zinc deficiency in tomato?
20. How to control late blight in tomato?
21. What is the fertilizer ratio for banana vegetative stage?
22. What is the fertilizer ratio for banana bunch development stage?
23. How does Zetol Select improve banana fruit quality?
24. What are the benefits of Trail Blaze for chilli?
25. What are the benefits of Actin Granules for chilli?
26. How to apply Actin Granules for chilli?
27. When to spray Akre Shield on chilli?
28. How to control root rot in chilli?
29. How to control fusarium wilt in chilli?
30. How to control aphids in chilli?
31. How to control flower drop in chilli?
32. What is the dosage of Diafenthiuron for chilli?
33. What is the dosage of Triazophos for chilli?
34. What are the benefits of Akre Shield for tomato?
35. How to control early blight in tomato?
36. How to control iron deficiency in tomato?
37. What is the dosage of Actin Granules for banana?
38. How to control sigatoka leaf spot in banana?
39. How to control nematodes in banana?
40. What is the dosage of Carbofuron for banana?

---

## Scenario 1B: Agriculture without Context (15 scenarios)
*Agricultural topics NOT covered in the FAQ - should return "I don't know..."*

1. How to grow organic wheat in sandy soil?
2. What is the best variety of rice for coastal areas?
3. How to control stem borer in sugarcane?
4. What fertilizer is best for cotton cultivation?
5. How to manage water logging in paddy fields?
6. What is the spacing for maize plantation?
7. How to control aphids in mustard crop?
8. What is the harvesting time for groundnut?
9. How to store onions after harvest?
10. What is the seed rate for soybean cultivation?
11. How to control pink bollworm in cotton?
12. What is the irrigation schedule for wheat?
13. How to manage nitrogen deficiency in corn?
14. What pesticide is effective against armyworm?
15. How to increase protein content in pulses?

---

## Scenario 2: Non-Agriculture (15 scenarios)
*Non-agricultural topics that should be rejected*

1. How to lose weight quickly?
2. Best smartphones under 20000 rupees
3. How to learn Python programming?
4. What are the symptoms of diabetes?
5. How to book train tickets online?
6. Best places to visit in Kerala
7. How to start a YouTube channel?
8. What is the weather forecast for tomorrow?
9. How to prepare for UPSC exam?
10. Best laptops for gaming in 2024
11. How to cook chicken biryani?
12. What are the latest fashion trends?
13. How to get a driving license?
14. Best investment options for beginners
15. How to improve English speaking skills?

---

## Expected Performance

### Response Types:
- **Scenario 1A**: AGRICULTURE_WITH_CONTEXT → Specific, accurate answers from FAQ
- **Scenario 1B**: NO_RELEVANT_CHUNKS → "I don't know. I can help you by transferring the call to subject matter expertise if needed."
- **Scenario 2**: NON_AGRICULTURE → "I can answer only agriculture related queries."

### Performance Targets:
- **First Run**: <1.2 seconds (IVR requirement)
- **Second Run**: <0.9 seconds (cached response)
- **Intent Accuracy**: 100% correct classification
- **Answer Accuracy**: Grounded in FAQ content only

### Testing Instructions:
1. Test each scenario in Streamlit interface
2. Verify intent classification is correct
3. Verify response content matches expected type
4. Check that second run is faster than first run
5. Ensure vocabulary corrections work for mispronounced terms

---

## Vocabulary Test Cases
*Test these with intentional mispronunciations to verify correction system*

1. "What is Dormolin Vegetative used for?" → Should correct to "Dormulin"
2. "How much Acre Shield for chilli?" → Should correct to "Akre Shield"  
3. "What is Tracks Sure dosage?" → Should correct to "Tracs Sure"
4. "How to control trips in chili?" → Should correct to "thrips in chilli"
5. "What is Acting granules dosage?" → Should correct to "Actin granules"