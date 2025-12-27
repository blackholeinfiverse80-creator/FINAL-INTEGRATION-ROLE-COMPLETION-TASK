# Demo Video Script - Core Integrator (2-3 minutes)

## 🎬 RECORDING SETUP

### Before Recording:
1. **Start Services:**
   ```bash
   # Terminal 1: Start Noopur Service
   cd external/CreatorCore-Task
   python app.py
   
   # Terminal 2: Start Mock CreatorCore
   cd tests/mocks
   python creatorcore_mock.py
   
   # Terminal 3: Main demo terminal
   cd Core-Integrator-Sprint-1.1-
   ```

2. **Screen Setup:**
   - Close unnecessary applications
   - Set terminal font size to 14+ for visibility
   - Have 2-3 terminal windows ready
   - Browser ready for health endpoints

### Recording Tools:
- **Windows:** Built-in Xbox Game Bar (Win+G) or OBS Studio
- **Screen Resolution:** 1920x1080 recommended
- **Audio:** Clear narration explaining each step

## 📝 DEMO SCRIPT (2-3 minutes)

### Scene 1: Introduction (15 seconds)
**Narration:** "This is the Core Integrator AI Request Enhancement Pipeline demo. I'll show you the complete flow from user request to AI-enhanced response."

**Actions:**
- Show project structure briefly
- Highlight key components: src/, tests/, documentation/

### Scene 2: Start Services (30 seconds)
**Narration:** "First, let's start our services. The Noopur AI backend on port 5001, and the CreatorCore mock server on port 5002."

**Actions:**
```bash
# Show starting Noopur (already running)
curl http://localhost:5001/history

# Show starting Mock CreatorCore
python tests/mocks/creatorcore_mock.py
# In another terminal:
curl http://localhost:5002/system/health
```

### Scene 3: Prompt → Output Flow (45 seconds)
**Narration:** "Now I'll demonstrate the core flow: sending a creative request through the integrator to get AI-enhanced responses."

**Actions:**
```python
# Run this in Python terminal
import sys
sys.path.append('.')
from creator_routing import CreatorRouter

# Create router
router = CreatorRouter()

# Send request
request_data = {
    "topic": "Artificial Intelligence",
    "goal": "Create educational tutorial", 
    "type": "article"
}

print("Input Request:")
print(request_data)

# Process through router
result = router.prewarm_and_prepare("generate", "demo_user", request_data)

print("\nAI-Enhanced Response:")
print(result)
```

**Show:** Input request → Enhanced response with related_context

### Scene 4: Feedback Processing (30 seconds)
**Narration:** "The system also handles feedback to improve future responses."

**Actions:**
```python
# Send feedback
feedback_data = {
    "user_id": "demo_user",
    "rating": 5,
    "comment": "Excellent AI enhancement"
}

feedback_result = router.forward_feedback({
    "generation_id": 1,
    "command": "+1"
})

print("Feedback Result:")
print(feedback_result)
```

### Scene 5: Bridge Logs & Health (30 seconds)
**Narration:** "Let's check the bridge connectivity and system health."

**Actions:**
```python
# Test bridge client
from src.utils.bridge_client import BridgeClient

bridge = BridgeClient("http://localhost:5002")

# Health check
health = bridge.health_check()
print("Bridge Health:")
print(health)

# Log something
log_result = bridge.log({
    "level": "info",
    "message": "Demo completed successfully",
    "component": "core_integrator"
})
print("Log Result:")
print(log_result)
```

### Scene 6: Mock Environment Demo (20 seconds)
**Narration:** "The system works seamlessly with mock services for testing."

**Actions:**
```bash
# Show mock server debug endpoints
curl http://localhost:5002/debug/logs
curl http://localhost:5002/debug/feedback
```

**Show:** Mock server data, demonstrating test environment

### Scene 7: Coverage & Testing (10 seconds)
**Narration:** "Finally, our comprehensive test suite ensures reliability."

**Actions:**
```bash
# Show test results
python run_coverage_report.py
```

**Show:** Test results, coverage report briefly

## 🎯 KEY POINTS TO HIGHLIGHT

### Technical Features:
- ✅ AI-powered context enhancement
- ✅ Multi-service integration (Noopur + CreatorCore)
- ✅ Robust error handling and retry logic
- ✅ Mock environment for testing
- ✅ Comprehensive logging and health monitoring

### Architecture Benefits:
- ✅ Microservices design
- ✅ Fallback mechanisms
- ✅ Real-time AI processing
- ✅ Scalable integration patterns

## 📋 RECORDING CHECKLIST

### Pre-Recording:
- [ ] All services running (Noopur + Mock)
- [ ] Terminal fonts readable
- [ ] Screen recording software ready
- [ ] Script practiced once

### During Recording:
- [ ] Clear narration
- [ ] Show input → processing → output
- [ ] Demonstrate error handling
- [ ] Show health endpoints
- [ ] Keep under 3 minutes

### Post-Recording:
- [ ] Save as MP4 format
- [ ] File size under 50MB
- [ ] Audio quality good
- [ ] All demo points covered

## 🎬 FINAL VIDEO STRUCTURE

1. **Intro** (15s) - Project overview
2. **Services** (30s) - Start Noopur + Mock
3. **Core Flow** (45s) - Request → AI Enhancement
4. **Feedback** (30s) - Feedback processing
5. **Health** (30s) - Bridge logs & health
6. **Mock Demo** (20s) - Mock environment
7. **Testing** (10s) - Coverage results

**Total: ~3 minutes**

## 📁 SAVE VIDEO AS:
`core_integrator_demo_video.mp4`