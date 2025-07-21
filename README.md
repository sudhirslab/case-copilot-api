# case-copilot-api
A Chat Application Backend that handles and support opening a case and chatting with staff members and the AI assistant.

## Objective

This allow a logged-in user to open a new case for a specific healthcare issue that they want our help with. Once opened, a case will be presented to the user as a standard chat UX in our web and mobile apps. You will focus on creating data models and an API service to support opening a case and chatting with Medbill AI staff members and the AI assistant.

The basic considerations for the service should include:

- Users,Office staff, and AI assistants can all interact with a case via the API. However, each case is owned by a specific user.
    - Note that direct user-to-user messaging is not allowed.
- Users and staff members can attach files (images and documents) to a case.

- A user may open multiple cases.
- Chat messages and attachments belong to a case. Maintaining a separate “chat” concept is not necessary - the UX for a case is a chat conversation.
- User able to attach files