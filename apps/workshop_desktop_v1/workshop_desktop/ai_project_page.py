"""Opt-in AI project description UI. Planning only; no repository writes."""
import threading
import tkinter as tk
from tkinter import ttk

from .ollama_provider import OllamaTextProvider, ProviderError


class AIProjectPage(ttk.Frame):
    """A non-destructive entry point for a plain-language project description."""

    def __init__(self, master):
        super().__init__(master, padding=14)
        self._busy = False
        self.name = tk.StringVar()
        self.model = tk.StringVar(value="")
        self.status = tk.StringVar(value="Local model only. No code or files will be changed.")
        ttk.Label(self, text="Create AI Project", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))
        ttk.Label(self, text="Project name").pack(anchor="w")
        ttk.Entry(self, textvariable=self.name, width=60).pack(fill="x", pady=(2, 9))
        ttk.Label(self, text="Describe what you want to build").pack(anchor="w")
        self.description = tk.Text(self, height=7, wrap="word")
        self.description.pack(fill="x", pady=(2, 9))
        ttk.Label(self, text="Local Ollama model name (already installed)").pack(anchor="w")
        ttk.Entry(self, textvariable=self.model, width=40).pack(fill="x", pady=(2, 9))
        ttk.Label(self, text="This first integration creates a suggested plan for review. It does not execute code or use paid services.", wraplength=900).pack(anchor="w", pady=(0, 10))
        self.start = ttk.Button(self, text="Generate project outline (local)", command=self.generate_outline)
        self.start.pack(anchor="w")
        ttk.Label(self, textvariable=self.status, wraplength=900).pack(anchor="w", pady=8)
        self.output = tk.Text(self, height=15, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True, pady=8)

    def generate_outline(self):
        if self._busy:
            return
        project = self.name.get().strip()
        description = self.description.get("1.0", "end-1c").strip()
        model = self.model.get().strip()
        if not project or not description or not model:
            self.status.set("Enter a project name, description and local model.")
            return
        if len(project) > 120 or len(description) > 20000:
            self.status.set("Project name or description is too long.")
            return
        self._busy = True
        self.start.configure(state="disabled")
        self.status.set("Requesting a planning outline from your local model...")
        prompt = (
            "Prepare a concise engineering project outline, not code execution. "
            "Include scope, prerequisites, protected components, bounded first task, "
            "test criteria and unknowns. Do not claim anything was implemented.\n"
            "Project: " + project + "\nRequest: " + description
        )

        def worker():
            try:
                result = OllamaTextProvider(model).generate(prompt)
                message = result.content
                status = "Outline generated locally. Review before taking any action."
            except (ProviderError, ValueError):
                message = ""
                status = "Local Ollama unavailable or invalid response. Verify Ollama and the model name."
            self.after(0, lambda: self._finish(message, status))

        threading.Thread(target=worker, daemon=True).start()

    def _finish(self, message, status):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", message)
        self.output.configure(state="disabled")
        self.status.set(status)
        self._busy = False
        self.start.configure(state="normal")
