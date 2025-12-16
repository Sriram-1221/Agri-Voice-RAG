#!/usr/bin/env python3
"""
Warm cache for ALL scenarios (1A + 1B) from SCENARIOS_STREAMLIT.md
"""

from contextual_knowledge_engine import contextual_engine, setup_contextual_knowledge_engine
import time

def warm_all_scenarios():
    """Pre-cache ALL scenarios for lightning-fast demo"""
    
    # ALL Scenario 1A queries (40 total)
    scenario_1a_queries = [
        "What is Dormulin Vegetative used for?",
        "What is Dormulin Flowering designed for?",
        "What is the fertilizer ratio for banana rooting stage?",
        "What are the benefits of Zetol Select for banana vegetative stage?",
        "What is the dosage of Trail Blaze for chilli seeds?",
        "How much Actin Granules should be applied per acre for chilli?",
        "What is the dosage of Tracs Sure for chilli?",
        "What is the foliar spray dosage of Zetol Select for chilli?",
        "What is the dosage of Akre Shield for chilli?",
        "How to control damping-off in chilli?",
        "How to control bacterial leaf spot in chilli?",
        "How to control powdery mildew in chilli?",
        "How to control thrips and mites in chilli?",
        "How to control whiteflies in chilli?",
        "How to control fruit borer in chilli?",
        "What is the seed treatment dosage for Trail Blaze in tomato?",
        "How much Actin Granules for tomato per acre?",
        "How to control potash deficiency in tomato?",
        "How to control zinc deficiency in tomato?",
        "How to control late blight in tomato?",
        "What is the fertilizer ratio for banana vegetative stage?",
        "What is the fertilizer ratio for banana bunch development stage?",
        "How does Zetol Select improve banana fruit quality?",
        "What are the benefits of Trail Blaze for chilli?",
        "What are the benefits of Actin Granules for chilli?",
        "How to apply Actin Granules for chilli?",
        "When to spray Akre Shield on chilli?",
        "How to control root rot in chilli?",
        "How to control fusarium wilt in chilli?",
        "How to control aphids in chilli?",
        "How to control flower drop in chilli?",
        "What is the dosage of Diafenthiuron for chilli?",
        "What is the dosage of Triazophos for chilli?",
        "What are the benefits of Akre Shield for tomato?",
        "How to control early blight in tomato?",
        "How to control iron deficiency in tomato?",
        "What is the dosage of Actin Granules for banana?",
        "How to control sigatoka leaf spot in banana?",
        "How to control nematodes in banana?",
        "What is the dosage of Carbofuron for banana?"
    ]
    
    # ALL Scenario 1B queries (15 total)
    scenario_1b_queries = [
        "How to grow organic wheat in sandy soil?",
        "What is the best variety of rice for coastal areas?",
        "How to control stem borer in sugarcane?",
        "What fertilizer is best for cotton cultivation?",
        "How to manage water logging in paddy fields?",
        "What is the spacing for maize plantation?",
        "How to control aphids in mustard crop?",
        "What is the harvesting time for groundnut?",
        "How to store onions after harvest?",
        "What is the seed rate for soybean cultivation?",
        "How to control pink bollworm in cotton?",
        "What is the irrigation schedule for wheat?",
        "How to manage nitrogen deficiency in corn?",
        "What pesticide is effective against armyworm?",
        "How to increase protein content in pulses?"
    ]
    
    print("🚀 Warming cache for ALL scenarios (1A + 1B)...")
    print("=" * 60)
    
    # Setup engine
    if not setup_contextual_knowledge_engine():
        print("❌ Failed to setup contextual knowledge engine")
        return False
    
    total_start = time.time()
    cached_count = 0
    
    # Cache Scenario 1A queries
    print("🌱 Caching Scenario 1A queries (Agriculture with Context)...")
    for i, query in enumerate(scenario_1a_queries, 1):
        print(f"🔄 1A-{i:2d}/40: {query[:50]}...")
        
        try:
            start_time = time.time()
            result = contextual_engine.process_contextual_query(query)
            process_time = time.time() - start_time
            
            print(f"   ✅ Cached in {process_time:.2f}s - Intent: {result['intent']}, Type: {result['response_type']}")
            cached_count += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🌾 Caching Scenario 1B queries (Agriculture without Context)...")
    for i, query in enumerate(scenario_1b_queries, 1):
        print(f"🔄 1B-{i:2d}/15: {query[:50]}...")
        
        try:
            start_time = time.time()
            result = contextual_engine.process_contextual_query(query)
            process_time = time.time() - start_time
            
            print(f"   ✅ Cached in {process_time:.2f}s - Intent: {result['intent']}, Type: {result['response_type']}")
            cached_count += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    total_time = time.time() - total_start
    total_queries = len(scenario_1a_queries) + len(scenario_1b_queries)
    
    print("\n" + "=" * 60)
    print(f"🎯 Cache warming complete!")
    print(f"📊 Cached queries: {cached_count}/{total_queries}")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"⚡ Average time per query: {total_time/cached_count:.2f}s")
    
    return cached_count >= (total_queries - 5)  # Allow for some failures

def warm_audio_cache():
    """Pre-warm audio cache for common responses"""
    print("\n🔊 Warming audio cache for common responses...")
    
    try:
        from voice_interface import VoiceInterface
        voice_interface = VoiceInterface()
        
        common_responses = [
            "I can answer only agriculture related queries.",
            "I don't know. I can help you by transferring the call to subject matter expertise if needed.",
            "Dormulin Vegetative is used to promote strong root and shoot growth, healthy green leaves, and overall vigorous development.",
            "5 ml of Trail Blaze per 100 g of seed for chilli seed treatment.",
            "3 kg/acre of Actin Granules should be applied for chilli.",
            "Foliar spray with Triazophos 400 ml/acre or Carbosulfan 400 ml/acre for fruit borer control."
        ]
        
        for i, response in enumerate(common_responses, 1):
            print(f"🔊 Audio {i}/{len(common_responses)}: {response[:40]}...")
            audio_file = voice_interface._get_cached_audio(response)
            if audio_file:
                print(f"   ✅ Audio cached: {audio_file}")
            else:
                print(f"   ❌ Audio failed")
        
        print("🔊 Audio cache warming complete!")
        return True
        
    except Exception as e:
        print(f"❌ Audio cache warming failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive cache warming...")
    
    # Warm query cache
    query_success = warm_all_scenarios()
    
    # Warm audio cache
    audio_success = warm_audio_cache()
    
    if query_success and audio_success:
        print("\n🎉 ALL SCENARIOS CACHED SUCCESSFULLY!")
        print("🚀 Demo will now be lightning fast for ALL queries!")
        print("⚡ Both text and voice interfaces are optimized!")
    else:
        print("\n⚠️ Some caching failed, but system should still work")
    
    print("\n💡 Ready for demo at http://localhost:8501")