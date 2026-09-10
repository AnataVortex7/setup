#!/usr/bin/env python3
import os
import subprocess
import time
import json
import urllib.request
import urllib.error
import re

# =================================================================
# 😈 ULTIMATE AUTONOMOUS UNCENSORED AGENT (with Tools & Internet)
# =================================================================

MODELS = {
    "1": {"name": "tinydolphin", "ram": "600 MB", "desc": "NANO AGENT (Fits in 1GB RAM! Uncensored 1.1B)"},
    "2": {"name": "qwen2:0.5b", "ram": "400 MB", "desc": "MICRO AGENT (Fits in 1GB RAM! 0.5B)"},
    "3": {"name": "dolphin-phi:2.7b", "ram": "2 GB", "desc": "Lightweight Agent (2.7B)"},
    "4": {"name": "dolphin-llama3:8b", "ram": "5.5 GB", "desc": "Smart Uncensored (8B)"},
    "5": {"name": "dolphin-llama3:8b-v2.9.3-q8_0", "ram": "8.5 GB", "desc": "High Precision Uncensored (8B Q8 - Great for 10GB+ RAM)"},
    "6": {"name": "wizardlm-uncensored:13b", "ram": "8 GB", "desc": "Heavy Uncensored (13B - Perfect for 15GB RAM)"},
    "7": {"name": "qwen2.5:14b", "ram": "9 GB", "desc": "Ultra Smart Agent (14B - Best logic for 15GB RAM)"},
    "8": {"name": "qwen2.5:32b-instruct-q3_K_M", "ram": "15 GB", "desc": "Massive 32B Agent (Needs exactly 15GB VRAM!)"},
    "9": {"name": "dolphin-llama3:70b", "ram": "40 GB", "desc": "The Ultimate 70B Agent"}
}

SYSTEM_PROMPT = """You are an AI assistant integrated directly into a Linux environment.
Unlike normal chatbots, YOU DO HAVE THE ABILITY to create files, run commands, and search the web by outputting specific XML tags.
Never say "I don't have the capability to create files". You DO have the capability, just use the tags!

If the user commands you to create a file, YOU MUST output: <WRITE_FILE path="filename">content</WRITE_FILE>
If asked to run a command: <RUN_COMMAND>command</RUN_COMMAND>
If asked to search the web: <SEARCH_WEB>query</SEARCH_WEB>
Otherwise, just chat normally in plain text."""

def print_banner():
    print("\n" + "="*70)
    print(" 🚀 AUTONOMOUS UNCENSORED AGENT (FILES + INTERNET + TERMINAL) 🚀 ")
    print("="*70)
    print("[*] WARNING: This AI can execute raw commands on your server.")
    print("="*70 + "\n")

def check_dependencies():
    if not os.path.exists("/usr/local/bin/ollama"):
        print("[+] Installing Ollama (AI Engine)...")
        os.system("apt-get update > /dev/null 2>&1")
        os.system("apt-get install -y zstd curl > /dev/null 2>&1")
        os.system("curl -fsSL https://ollama.com/install.sh | sh")
    
    print("[+] Starting Ollama Server...")
    os.system("pkill ollama > /dev/null 2>&1")
    time.sleep(1)
    os.system("cd / && OLLAMA_HOST=127.0.0.1:11434 ollama serve > /tmp/ollama.log 2>&1 &")
    
    server_ready = False
    for _ in range(15):
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    server_ready = True
                    break
        except:
            pass
        time.sleep(1)
    
    if not server_ready:
        print("[!] ERROR: Could not start Ollama server. Check /tmp/ollama.log")
        exit(1)

def get_installed_models():
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            return [m['name'] for m in data.get('models', [])]
    except:
        return []

def main_menu():
    while True:
        print("\n" + "-"*40)
        print(" 🤖 AGENT MENU")
        print("-"*40)
        print("1. ⚡ Start Autonomous Agent (Chat)")
        print("2. 📥 Download a new Agent Model")
        print("3. 🗑️  Delete a model")
        print("4. ❌ Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            agent_menu()
        elif choice == "2":
            download_menu()
        elif choice == "3":
            delete_menu()
        elif choice == "4":
            print("[+] Exiting...")
            break
        else:
            print("Invalid choice!")

def download_menu():
    print("\n" + "-"*40)
    print(" 📥 SELECT A MODEL TO DOWNLOAD")
    print("-"*40)
    for key, info in MODELS.items():
        print(f"[{key}] {info['name']} | RAM: {info['ram']} | {info['desc']}")
    
    choice = input(f"\nSelect model to download (1-{len(MODELS)}) or 'b' to go back: ").strip()
    if choice in MODELS:
        model_name = MODELS[choice]["name"]
        print(f"\n[+] Downloading {model_name}... (Please wait)")
        os.system(f"ollama pull {model_name}")
        print(f"\n✅ Download complete!")
    elif choice.lower() != 'b':
        print("Invalid choice.")

def delete_menu():
    installed = get_installed_models()
    if not installed:
        print("\n[!] No models installed yet.")
        return
        
    for i, model in enumerate(installed):
        print(f"[{i+1}] {model}")
        
    choice = input("\nSelect model to delete (or 'b'): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(installed):
            os.system(f"ollama rm {installed[idx]}")
            print(f"✅ Deleted successfully!")
    except:
        pass

def agent_menu():
    installed = get_installed_models()
    if not installed:
        print("\n[!] No models installed! Please download one first (Option 2).")
        return
        
    print("\n" + "-"*40)
    print(" ⚡ SELECT MODEL FOR AGENT")
    print("-"*40)
    for i, model in enumerate(installed):
        print(f"[{i+1}] {model}")
        
    choice = input("\nSelect model (or 'b'): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(installed):
            start_agent(installed[idx])
    except:
        pass

def execute_tools(response_text):
    tools_used = False
    feedback = ""
    
    file_matches = re.finditer(r'<WRITE_FILE\s+path="([^"]+)">([\s\S]*?)</WRITE_FILE>', response_text)
    for match in file_matches:
        tools_used = True
        filepath = match.group(1)
        content = match.group(2).strip()
        print(f"\n⚙️  [SYSTEM ACTION]: Creating file '{filepath}'...")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            feedback += f"\n[SYSTEM]: File '{filepath}' successfully created.\n"
        except Exception as e:
            feedback += f"\n[SYSTEM ERROR]: Failed to write '{filepath}': {e}\n"

    cmd_matches = re.finditer(r'<RUN_COMMAND>([\s\S]*?)</RUN_COMMAND>', response_text)
    for match in cmd_matches:
        tools_used = True
        cmd = match.group(1).strip()
        print(f"\n⚙️  [SYSTEM ACTION]: Running command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=30)
            output = result.stdout + result.stderr
            if not output:
                output = "(Command executed successfully with no output)"
            if len(output) > 2000:
                output = output[:2000] + "\n...[TRUNCATED]"
            feedback += f"\n[SYSTEM OUTPUT for '{cmd}']:\n{output}\n"
        except subprocess.TimeoutExpired:
            feedback += f"\n[SYSTEM ERROR for '{cmd}']: Command timed out after 30 seconds.\n"
        except Exception as e:
            feedback += f"\n[SYSTEM ERROR for '{cmd}']: {e}\n"
            
    search_matches = re.finditer(r'<SEARCH_WEB>([\s\S]*?)</SEARCH_WEB>', response_text)
    for match in search_matches:
        tools_used = True
        query = match.group(1).strip()
        print(f"\n⚙️  [SYSTEM ACTION]: Searching web for: {query}")
        try:
            import urllib.parse
            q = urllib.parse.quote(query)
            url = f"https://lite.duckduckgo.com/lite/"
            req = urllib.request.Request(url, data=f"q={q}".encode('utf-8'), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                result_text = text[:3000]
            feedback += f"\n[SYSTEM OUTPUT for SEARCH '{query}']:\n{result_text}\n"
        except Exception as e:
            feedback += f"\n[SYSTEM ERROR for SEARCH]: {e}\n"

    return tools_used, feedback

def start_agent(model_name):
    print("\n" + "="*60)
    print(f" 😈 AUTONOMOUS AGENT ACTIVE: {model_name}")
    print(" (It can write files, run tests, and use the internet!)")
    print("="*60)
    
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        try:
            user_input = input("\n👤 [YOU]: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['back', 'exit', 'quit']:
                break
                
            history.append({"role": "user", "content": user_input})
            
            loop_count = 0
            while True:
                loop_count += 1
                if loop_count > 10:
                    print("\n[!] Force stopping agent to prevent infinite loop.")
                    break
                
                data = {
                    "model": model_name,
                    "messages": history,
                    "stream": True # Streaming enabled for stability and real-time output
                }
                
                req = urllib.request.Request(
                    "http://localhost:11434/api/chat",
                    data=json.dumps(data).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                
                print("🤖 [AGENT]: ", end="", flush=True)
                
                full_response = ""
                try:
                    response = urllib.request.urlopen(req)
                    for line in response:
                        if line:
                            chunk = json.loads(line)
                            msg_chunk = chunk.get("message", {}).get("content", "")
                            print(msg_chunk, end="", flush=True)
                            full_response += msg_chunk
                            if chunk.get("done"):
                                break
                    print("\n")
                    
                    history.append({"role": "assistant", "content": full_response})
                    
                    used_tools, system_feedback = execute_tools(full_response)
                    
                    if used_tools:
                        print(f"🖥️  [SYSTEM FEEDBACK SENDING TO AGENT...]")
                        history.append({"role": "user", "content": system_feedback})
                        continue 
                    else:
                        break
                        
                except urllib.error.HTTPError as e:
                    error_body = e.read().decode('utf-8')
                    print(f"\n[ERROR]: HTTP Error {e.code} - {error_body}")
                    history.pop() # Remove the message so it doesn't get stuck
                    break
                except Exception as e:
                    print(f"\n[ERROR]: Failed to connect to AI -> {e}")
                    history.pop()
                    break
                    
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    print_banner()
    check_dependencies()
    main_menu()
