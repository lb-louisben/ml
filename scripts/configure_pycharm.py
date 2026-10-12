"""Configure local PyCharm source roots without changing code or global SDKs.

Close the project in PyCharm, then run from the checkout:
python3 scripts/configure_pycharm.py
Local .idea files stay ignored by Git. Rerun after copying an NJU assignment
into work/ so each existing src package belongs to a separate module.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = ('.git', '.idea', '.venv', '.venv-dl', 'venv', '.cache', '.jupyter',
            '__pycache__', '.ipynb_checkpoints', '.pytest_cache', '.mypy_cache',
            '.ruff_cache', 'outputs', 'checkpoints', 'runs', 'logs', 'wandb',
            'downloads', 'node_modules', 'model', 'datasets')


def file_url(path):
    # JetBrains VFS URLs keep spaces literal; XML handles escaping.
    return 'file://' + path.resolve().as_posix()


def read_xml(path, tag, **attributes):
    if path.exists():
        return ET.parse(path).getroot()
    return ET.Element(tag, attributes)


def component(tree, name):
    existing = tree.find(f"./component[@name='{name}']")
    return existing if existing is not None else ET.SubElement(tree, 'component', name=name)


def save_xml(path, tree):
    ET.indent(tree, space='  ')
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' +
                    ET.tostring(tree, encoding='unicode') + '\n', encoding='utf-8')


def configure(root):
    root = root.resolve()
    idea = root / '.idea'
    idea.mkdir(exist_ok=True)
    main_path = idea / f'{root.name}.iml'
    module = read_xml(main_path, 'module', type='PYTHON_MODULE', version='4')
    manager = component(module, 'NewModuleRootManager')
    sdk = manager.find("./orderEntry[@type='jdk']")
    misc_path = idea / 'misc.xml'
    misc = read_xml(misc_path, 'project', version='4')
    if sdk is not None and sdk.get('jdkName'):
        project_sdk = component(misc, 'ProjectRootManager')
        project_sdk.set('version', '2')
        project_sdk.set('project-jdk-name', sdk.get('jdkName'))
        project_sdk.set('project-jdk-type', 'Python SDK')
        save_xml(misc_path, misc)

    tasks = []
    for parent in ('assignments/nju-llm-2026', 'work/nju-llm-2026'):
        for number in range(6):
            path = root / parent / f'a{number}'
            if path.is_dir():
                tasks.append(path.relative_to(root).as_posix())

    for item in list(manager):
        if item.tag in {'content', 'orderEntry'}:
            manager.remove(item)
    # Use explicit local URLs: PyCharm can normalize MODULE_DIR differently
    # for module files stored under .idea. These files never enter Git.
    content = ET.SubElement(manager, 'content', url=file_url(root))
    ET.SubElement(content, 'sourceFolder', url=file_url(root), isTestSource='false')
    if (root / 'assignments/bootcamp/week3').exists():
        ET.SubElement(content, 'sourceFolder', url=file_url(root / 'assignments/bootcamp/week3'), isTestSource='false')
    for name in EXCLUDED:
        ET.SubElement(content, 'excludePattern', pattern=name)
    for name in tasks:
        ET.SubElement(content, 'excludeFolder', url=file_url(root / name))
    ET.SubElement(manager, 'orderEntry', type='inheritedJdk')
    ET.SubElement(manager, 'orderEntry', type='sourceFolder', forTests='false')
    runner = component(module, 'TestRunnerService')
    option = runner.find("./option[@name='PROJECT_TEST_RUNNER']")
    if option is None:
        option = ET.SubElement(runner, 'option', name='PROJECT_TEST_RUNNER')
    option.set('value', 'py.test')
    save_xml(main_path, module)

    modules_path = idea / 'modules.xml'
    modules = read_xml(modules_path, 'project', version='4')
    registry = component(modules, 'ProjectModuleManager')
    entries = registry.find('modules')
    if entries is None:
        entries = ET.SubElement(registry, 'modules')
    # Retain unrelated custom modules; replace only the main and our task modules.
    for entry in list(entries):
        filename = entry.get('filepath', '').split('/')[-1]
        if filename == main_path.name or filename.startswith('ml-study-task-'):
            entries.remove(entry)

    def register(path):
        value = '$PROJECT_DIR$/.idea/'+path.name
        ET.SubElement(entries, 'module', fileurl='file://'+value, filepath=value)

    register(main_path)
    for name in tasks:
        task_path = idea / ('ml-study-task-'+name.replace('/', '-')+'.iml')
        task_module = read_xml(task_path, 'module', type='PYTHON_MODULE', version='4')
        task_manager = component(task_module, 'NewModuleRootManager')
        for item in list(task_manager):
            if item.tag in {'content', 'orderEntry'}:
                task_manager.remove(item)
        task_content = ET.SubElement(task_manager, 'content', url=file_url(root / name))
        ET.SubElement(task_content, 'sourceFolder', url=file_url(root / name), isTestSource='false')
        for pattern in EXCLUDED:
            ET.SubElement(task_content, 'excludePattern', pattern=pattern)
        ET.SubElement(task_manager, 'orderEntry', type='inheritedJdk')
        ET.SubElement(task_manager, 'orderEntry', type='sourceFolder', forTests='false')
        save_xml(task_path, task_module)
        register(task_path)
    save_xml(modules_path, modules)
    return len(tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=ROOT)
    args = parser.parse_args()
    if not (args.repo_root / 'README.md').is_file():
        parser.error('请选择项目根目录，需包含 README.md')
    count = configure(args.repo_root)
    print(f'Configured PyCharm: project root + {count} isolated assignment modules.')
    print('Use the project .venv interpreter; reopen the project after configuration.')


if __name__ == '__main__':
    main()
