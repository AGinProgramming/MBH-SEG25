{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d059e119-2495-4003-a8e8-cf568af3937e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import tomllib   # Python 3.11+ 内置，如果是 Python <3.11 改用 \"import toml\"\n",
    "import subprocess\n",
    "\n",
    "def install_from_toml(toml_file=\"pyproject.toml\"):\n",
    "    # 读取 pyproject.toml\n",
    "    with open(toml_file, \"rb\") as f:\n",
    "        data = tomllib.load(f)\n",
    "\n",
    "    # 获取依赖\n",
    "    deps = data.get(\"project\", {}).get(\"dependencies\", [])\n",
    "    if not deps:\n",
    "        print(\"❌ 没找到依赖\")\n",
    "        return\n",
    "\n",
    "    print(\"📦 发现的直接依赖:\")\n",
    "    for dep in deps:\n",
    "        print(\"   -\", dep)\n",
    "\n",
    "    # 安装（不解析子依赖）\n",
    "    for dep in deps:\n",
    "        print(f\"\\n▶️ 安装 {dep} (忽略子依赖)\")\n",
    "        subprocess.run([\"pip\", \"install\", \"--no-deps\", dep])\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    install_from_toml(\"pyproject.toml\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
