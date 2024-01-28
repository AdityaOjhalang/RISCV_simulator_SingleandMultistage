```markdown
# 🚀 RV32I Simulator

Welcome to the RV32I Simulator repository! 🌟 This project, part of the ECE GY - 6913: Computing Systems Architecture course, now features both 🛠️ single-staged and 🖥️ five-staged pipeline architectures. It's designed to execute and analyze RISC-V test cases in these distinct pipeline configurations, making it a versatile tool for educational and research purposes.

## 📦 Dependencies

To get started, you'll need the following Python packages:

- `riscv-model==0.6.6`
- `bitstring~=4.0.1`

🔧 Install them via pip using:

```sh
pip3 install riscv-model==0.6.6
pip3 install bitstring~=4.0.1
```

👉 Make sure your pip is up-to-date to avoid any installation issues.

## 🚀 Running the Simulator

Follow these steps to launch your simulation:

1. 📁 Prepare an `input` directory at the root of the project with all the RISC-V test cases you want to simulate.
2. 🧭 Navigate to the project directory.
3. 🖥️ Run the `main.py` script with Python 3:

```sh
python3 netid/main.py
```

*Note: Replace `netid` with the directory name where your `main.py` file is located.*

4. The simulator now offers both 🛠️ single-stage and 🖥️ five-stage pipeline simulations. Choose your preferred mode when prompted or via a command-line argument.
5. 📈 After successful execution, the simulator will generate an `output` directory with the results for each test case.

## 📊 Output Format

The output provides detailed execution results for each test case. It demonstrates the inner workings of the chosen pipeline architecture (single-stage or five-stage) in a RISC-V processor.

## 👐 Contributing

Contributions to the RV32I Simulator are warmly welcomed! 🤝 If you're looking to contribute:

- Please adhere to the project's coding standards.
- Include tests for new features or bug fixes.

## 📬 Contact

Got questions or want to contribute? Feel free to reach out!

- 🙋‍♂️ Aditya Ojha
- 📧 aditya.ojha@nyu.edu

This README has been updated to reflect the addition of the five-stage pipeline architecture, enhancing the original single-stage pipeline functionality.
```
