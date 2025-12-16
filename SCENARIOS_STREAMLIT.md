# Agricultural FAQ RAG System - Test Scenarios

This document contains comprehensive test scenarios for the Agricultural FAQ RAG system to validate different response types and system behavior.

## Scenario Classification

### 1A: Agriculture with Context (50 scenarios)
Questions about topics covered in the FAQ document that should return specific answers with retrieved context.

### 1B: Agriculture without Context (40 scenarios) 
Agricultural questions not covered in the FAQ document that should return: "I don't know. I can help you by transferring the call to subject matter expertise if needed."

### 2: Non-Agriculture (40 scenarios)
Non-agricultural questions that should return: "I can answer only agriculture related queries."

---

## Scenario 1A: Agriculture with Context (50 scenarios)

1. What is Dormulin Vegetative used for?
2. How to control thrips in chilli?
3. What are the benefits of Zetol Select for banana?
4. How to treat bacterial leaf spot in chilli?
5. What is the dosage of Akre Shield for tomato?
6. How to apply Tracs Sure for chilli?
7. What are the stages of Zetol Select for banana?
8. How to control powdery mildew in chilli?
9. What is Trail Blaze used for in tomato?
10. How to control whiteflies in chilli?
11. What is Actin used for in banana?
12. How to treat root rot in chilli?
13. What are the benefits of Dormulin Flowering?
14. How to control aphids in chilli?
15. What is the fertilizer ratio for banana rooting stage?
16. How to treat early blight in tomato?
17. What is the dosage of Zetol Select for chilli?
18. How to control nematodes in banana?
19. What are chilli herbicides for pre-emergent control?
20. How to treat iron deficiency in tomato?
21. What is the application method for Akre Shield in chilli?
22. How to control fruit borer in chilli?
23. What are the benefits of Tracs Sure for banana?
24. How to treat damping-off in tomato nursery?
25. What is the dosage of Dormulin Vegetative for chilli?
26. How to control late blight in tomato?
27. What are the stages for Dormulin Flowering application?
28. How to treat zinc deficiency in tomato?
29. What is the fertilizer ratio for banana fruit development?
30. How to control rhizome weevil in banana?
31. What are the benefits of Trail Blaze for chilli seed treatment?
32. How to control red spider mite in tomato?
33. What is the application frequency for Dormulin Flowering?
34. How to treat zinc deficiency in tomato plants?
35. What are the herbicide options for tomato cultivation?
36. How to control sigatoka leaf spot in banana?
37. What is the dosage of Actin granules for chilli?
38. How to treat fusarium wilt in chilli plants?
39. What are the benefits of Zetol Select for banana vegetative stage?
40. How to control mealy bugs in tomato plants?
41. What is the application rate of Zetol Select for chilli?
42. How to prevent bacterial wilt in tomato?
43. What are the benefits of Akre Shield for banana protection?
44. How to control leaf curl virus in chilli?
45. What is the dosage of Trail Blaze for tomato seed treatment?
46. How to manage nutrient deficiency in banana plants?
47. What are the application stages of Tracs Sure?
48. How to control alternaria blight in chilli?
49. What is the frequency of Actin application in banana?
50. How to treat potash deficiency in tomato plants?

---

## Scenario 1B: Agriculture without Context (40 scenarios)

1. How to grow purple carrots in space?
2. What is the best fertilizer for dragon fruit cultivation?
3. How to control pests in quinoa farming?
4. What are the irrigation requirements for saffron?
5. How to grow vanilla beans in greenhouse?
6. What is the harvesting time for chia seeds?
7. How to control diseases in moringa cultivation?
8. What are the soil requirements for stevia farming?
9. How to grow black garlic commercially?
10. What is the best variety of purple corn?
11. How to control pests in spirulina farming?
12. What are the fertilizer needs for goji berries?
13. How to grow blue potatoes organically?
14. What is the irrigation schedule for amaranth?
15. How to control diseases in buckwheat farming?
16. What are the soil amendments for teff cultivation?
17. How to grow white strawberries in hydroponic system?
18. What is the best time to plant purple cauliflower?
19. How to control pests in millet farming?
20. What are the nutrient requirements for kohlrabi?
21. How to grow rainbow chard in vertical farming?
22. What is the harvesting method for fenugreek leaves?
23. How to control diseases in lentil cultivation?
24. What are the water requirements for chickpea farming?
25. How to grow purple basil commercially?
26. What is the best fertilizer for artichoke cultivation?
27. How to control pests in sesame farming?
28. What are the soil requirements for flax cultivation?
29. How to grow golden beets in container farming?
30. What is the irrigation method for sunflower cultivation?
31. How to cultivate black rice in organic farming?
32. What are the pest control methods for passion fruit?
33. How to grow white eggplant in greenhouse conditions?
34. What is the best soil preparation for turmeric cultivation?
35. How to control diseases in cardamom farming?
36. What are the fertilizer requirements for cashew trees?
37. How to grow purple sweet potatoes commercially?
38. What is the harvesting technique for black pepper?
39. How to control pests in cinnamon cultivation?
40. What are the irrigation needs for nutmeg farming?

---

## Scenario 2: Non-Agriculture (40 scenarios)

1. Budget smartphones under 30k
2. Best laptops for gaming in 2024
3. How to learn Python programming?
4. What are the top movies on Netflix?
5. Best restaurants in Mumbai
6. How to invest in stock market?
7. What is the weather forecast for tomorrow?
8. How to book flight tickets online?
9. Best universities for MBA in India
10. How to lose weight quickly?
11. What are the symptoms of diabetes?
12. How to repair a car engine?
13. Best places to visit in Europe
14. How to start a YouTube channel?
15. What is artificial intelligence?
16. How to cook biryani at home?
17. Best cricket players in the world
18. How to learn guitar online?
19. What are the latest fashion trends?
20. How to get a driving license?
21. Best mobile apps for productivity
22. How to write a resume?
23. What is cryptocurrency trading?
24. How to plan a wedding budget?
25. Best skincare routine for acne
26. How to learn digital marketing?
27. What are the benefits of yoga?
28. How to start an online business?
29. Best headphones under 5000 rupees
30. How to improve English speaking skills?
31. What are the top electric cars in India?
32. How to create a website using WordPress?
33. Best streaming services for movies and shows
34. How to prepare for UPSC civil services exam?
35. What are the symptoms of high blood pressure?
36. How to book train tickets online in India?
37. Best mutual funds for long-term investment
38. How to learn data science from scratch?
39. What are the latest iPhone features and price?
40. How to start a food delivery business?

---

## Expected Responses

### Scenario 1A Response Pattern:
- Intent: AGRICULTURE
- Response Type: AGRICULTURE_WITH_CONTEXT
- Answer: Specific information from FAQ document with context

### Scenario 1B Response Pattern:
- Intent: AGRICULTURE
- Response Type: NO_RELEVANT_CHUNKS
- Answer: "I don't know. I can help you by transferring the call to subject matter expertise if needed."

### Scenario 2 Response Pattern:
- Intent: NON_AGRICULTURE or AGRICULTURE (conservative classification)
- Response Type: NON_AGRICULTURE
- Answer: "I can answer only agriculture related queries."

---

## Performance Expectations

- **First Run**: 800-1547ms (realistic processing time)
- **Second Run**: 700-1100ms (optimized with caching)
- **Cache Hit Rate**: Natural caching after first run
- **Intent Accuracy**: Natural AI classification without forced caching