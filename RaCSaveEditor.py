import sys
from RaCSaveEditorForm import RaCSaveEditorForm

if __name__ == "__main__":
    args = sys.argv
    RaCSaveEditorForm(args[1] if len(args) > 1 else None).mainloop()