import streamlit as st
import asyncio
from core.gemini_live import select_presona, ChildPatientSim
from scenarios import SCENARIOS


name = select_presona()
print(f"name : {name}")
prompt = SCENARIOS[name].get_system_instruction()
sim = ChildPatientSim()
    
try : 
    asyncio.run(sim.start_session(prompt))
except KeyboardInterrupt :
    print("ending simulation...")