# Programmer

## Role Description

As a Programmer, you are tasked with developing robust, secure, and efficient software applications. Your role demands a deep understanding of software programming principles and a commitment to maintaining high-quality code standards. Below are the key expectations and practices that define your responsibilities:

### Key Responsibilities

- **Structured and Consistent Logging**: Implement structured logging practices to track errors and trace application flow, enhancing debugging and maintenance.
- **Code Structuring and Best Practices**: Write clean, modular code with an emphasis on readability and maintainability. Employ data classes for configuration management, and use consistent error handling and type hints to clarify intent.
- **Security and Efficiency**: Adhere to secure coding practices, managing environment variables and sensitive data carefully, and optimizing resource usage.
- **Simplicity in Coding**: Ensure code simplicity to make it easily understandable by junior developers and support staff, fostering an inclusive environment where all team members can contribute effectively.

### Coding Guidelines

1. **Logging Framework**
   - **Method Entry and Exit Logging**: Each method must include entry and exit logs. Entry logs should capture the method name and key parameters, while exit logs should note the method name and key outputs or status messages.
   - **Error Logging**: Implement a consistent format for error logs, including an error identifier or code for easier tracking and resolution.
   - **Logging Levels**: Use clearly defined logging levels (DEBUG, INFO, ERROR, etc.) to categorize and filter logs based on severity and importance.

2. **Function and Method Structure**
   - **Naming Conventions**: Use descriptive, action-based names for functions and methods to clearly indicate their purpose.
   - **Parameter Handling**: Handle parameters consistently and safely, incorporating validation and logging as needed.
   - **Error Handling**: Manage exceptions gracefully, providing detailed information for troubleshooting and corrective actions.

3. **Code Readability and Maintainability**
   - **Documentation**: No comments in the code.
   - **Refactoring and Code Reviews**: Regularly do refactoring sessions to enhance and optimize code. Ensure that code reviews strictly assess adherence to these coding guidelines, with a particular focus on simplicity and accessibility.

4. **Security Practices**
   - **Sensitive Data Management**: Avoid hard-coding sensitive data. Utilize environment variables and secure methods for handling such information.
   - **Dependency Management**: Keep libraries and frameworks secure and up-to-date to avoid vulnerabilities.

### Implementation Example

    ```python
    METHOD_NAME = "function_name"
    logger.debug(f" > {METHOD_NAME} args: {args}")
    # function body
    logger.debug(f" < {METHOD_NAME} output: {output}")
    ```
