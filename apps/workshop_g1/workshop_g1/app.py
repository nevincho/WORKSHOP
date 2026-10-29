"""Minimal Tkinter G1 viewer: no network, execution, Git or background services."""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from .core import create_workspace, inspect_workspace, verified_trust, G1Error


def main():
    root = tk.Tk()
    root.title('WORKSHOP Desktop — G1 Read-only')
    root.geometry('900x560')
    bundle = Path(__file__).parent / 'trusted'
    status = tk.StringVar(value='Select a workspace. Imported content is untrusted data.')
    bar = ttk.Frame(root, padding=12)
    bar.pack(fill='x')
    view = ttk.Treeview(root, columns=('id', 'project', 'status'), show='headings')
    for name in ('id','project','status'):
        view.heading(name, text=name.upper())
    view.pack(fill='both', expand=True, padx=12)
    info = tk.Text(root, height=6, state='disabled', wrap='word')
    info.pack(fill='x', padx=12, pady=4)
    ttk.Label(root, textvariable=status, padding=12).pack(fill='x')
    def inspect(directory):
        if not directory:
            return
        try:
            tasks, errors = inspect_workspace(directory, bundle)
            for item in view.get_children():
                view.delete(item)
            for filename, fields in tasks:
                view.insert('', 'end', values=(fields['TASK_ID'], fields['PROJECT'], fields['STATUS']))
            info.configure(state='normal')
            info.delete('1.0', 'end')
            info.insert('end', '\n'.join(f'{name}: {msg}' for name, msg in errors) or 'No diagnostics')
            info.configure(state='disabled')
            status.set(f'READ-ONLY: {directory} | tasks: {len(tasks)}, diagnostics: {len(errors)}')
        except (G1Error, OSError, ValueError) as e:
            messagebox.showerror('Read-only validation', str(e), parent=root)
    def create():
        parent = filedialog.askdirectory(title='Choose parent directory for new workspace')
        if not parent: return
        from tkinter import simpledialog
        name = simpledialog.askstring('New workspace', 'New empty directory name:', parent=root)
        if not name: return
        if '/' in name or '\\' in name or name in {'.','..'}:
            messagebox.showerror('Invalid name','Enter a single directory name', parent=root)
            return
        destination = Path(parent) / name
        if not messagebox.askyesno('Create workspace', f'Create exactly:\n{destination}\n  workspace.json\n  tasks/\n\nNo Git or network operations.', parent=root): return
        try:
            create_workspace(destination, bundle)
            inspect(destination)
        except (G1Error, OSError, ValueError) as e:
            messagebox.showerror('CREATE failed', str(e), parent=root)
    ttk.Button(bar, text='CREATE (new only)', command=create).pack(side='left', padx=5)
    ttk.Button(bar, text='OPEN (read-only)', command=lambda: inspect(filedialog.askdirectory(title='Open existing workspace'))).pack(side='left', padx=5)
    ttk.Button(bar, text='IMPORT / inspect (read-only)', command=lambda: inspect(filedialog.askdirectory(title='Inspect external directory'))).pack(side='left', padx=5)
    try: verified_trust(bundle)
    except Exception as e: status.set(f'TRUST ERROR: {e}; no task interpretation allowed')
    root.mainloop()

if __name__ == '__main__':
    main()
