import ast
import sys
from io import StringIO

FILE_PATH = r"C:\Users\geetl\OneDrive\Desktop\learning\ML\Python_code_techohartz\index.html"

def run_code(code):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        exec(code, {"__builtins__": __builtins__})
    except Exception:
        return None
    finally:
        sys.stdout = old_stdout
    return mystdout.getvalue()

def should_skip(code):
    c = code.strip()
    if not c:
        return True, "empty"
    lines = [ln for ln in c.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if not lines:
        return True, "comments only"
    if "input(" in c:
        return True, "uses input"
    if "plt.show()" in c or "matplotlib" in c:
        return True, "matplotlib"
    if "open(" in c and any(ext in c for ext in ["data.", "output.", ".txt", ".csv", ".json"]):
        return True, "file access"
    # Skip pip/virtualenv/comment blocks
    skip_keywords = ["pip install", "pip list", "pip uninstall", "python -m venv", "source ", "deactivate", "# TODO"]
    if any(kw in c for kw in skip_keywords):
        return True, "pip/virtualenv/placeholder"
    return False, ""

def fix_and_run(code):
    code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    skip, reason = should_skip(code)
    if skip:
        return None, None
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None, None
    assigned_names = []
    func_defs = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_names.append(target.id)
        elif isinstance(node, ast.FunctionDef):
            func_defs.append(node.name)
    lines = code.strip().splitlines()
    last_line = lines[-1].strip()
    modified = code
    if func_defs and not assigned_names:
        for fname in func_defs:
            modified += "\nprint(" + fname + "())"
    elif assigned_names and "print(" not in code:
        for name in assigned_names:
            modified += '\nprint("' + name + ':", ' + name + ")"
    output = run_code(modified)
    if output is not None and output.strip():
        return modified, output
    return None, None

def process_all():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    marker = '<pre><code class="language-python">'
    end_marker = '</code></pre>'
    result = []
    added = 0
    skipped = 0
    unchanged = 0
    i = content.find(marker)
    last_end = 0
    while i != -1:
        end = content.find(end_marker, i)
        if end == -1:
            break
        end_pos = end + len(end_marker)
        result.append(content[last_end:i])
        j = end_pos
        while j < len(content) and content[j] in ' \n\t':
            j += 1
        has_output = content[j:j+len('<div class="box box-green"')] == '<div class="box box-green"'
        code_block = content[i + len(marker):end]
        code_clean = code_block.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        if has_output:
            result.append(content[i:end_pos])
            last_end = end_pos
            i = content.find(marker, end_pos)
            continue
        new_code, output = fix_and_run(code_clean)
        if new_code is not None and output:
            new_code_html = new_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            output_html = output.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append(marker + new_code_html + end_marker + "\n")
            result.append(
                '                <div class="box box-green" style="margin-top: 15px;">\n'
                '                    <h4>Output</h4>\n'
                '                    <pre><code>' + output_html + '</code></pre>\n'
                '                </div>'
            )
            added += 1
        else:
            skip, reason = should_skip(code_clean)
            if skip:
                skipped += 1
            else:
                unchanged += 1
            result.append(content[i:end_pos])
        last_end = end_pos
        i = content.find(marker, end_pos)
    result.append(content[last_end:])
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(''.
{snip}
    print(f"Done. Added output to: {added}. Skipped: {skipped}. Unchanged: {unchanged}.")

if __name__ == "__main__":
    process_all()
