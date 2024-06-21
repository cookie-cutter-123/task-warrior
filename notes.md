Please keep in mind that I have not used Python for years.
My goal was to demonstrate how a project like this can be structured and to write some scenarios to test the application.

#### Some of the things I would do if I had more time:

- Check all commands from `task help` and write tests for each of them.
- Write tests for different combinations of arguments passed to the task CLI.
- Write negative test cases, e.g., non-existing arguments, IDs, etc.
- Later on: performance and penetration tests.

#### Additional Scenarios to Consider:

- Verify the task counter accuracy.
- After completing a non-priority task, check if the message "You have more urgent tasks" is displayed.
- For task done by name, verify the completion message and ensure the task does not appear in subsequent listings (negative check).
- For task done by ID, verify the completion message and ensure the task does not appear in subsequent listings (negative check).
- Test if setting priority to High adds Urgency = 6.
- Check if the task <id> status includes all 8 fields: ID, Description, Status, Entered, Last Modified, Virtual Tags, UUID, Urgency, and Priority.
