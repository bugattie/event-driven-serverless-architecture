# Serverless Event-Driven Architecture with AWS SAM

This project demonstrates a **serverless event-driven architecture** using AWS SAM and several AWS services. The goal is to build a highly decoupled and modular system for event processing, showcasing the power of serverless technology.

---

## Phase One: Emitting an Event

### API Gateway

- Set up an **Amazon API Gateway** to expose a REST API endpoint that allows external systems to send event data into the workflow.

### Amazon SQS

- Integrated an **Amazon Simple Queue Service (SQS)** to decouple the components, ensuring reliability and scalability for event delivery.

### Lambda Function

- Developed a Lambda function (`EmitOrderEventFunction`) to process the event payload received from the SQS queue.
- The Lambda function validates and enriches the event before putting it into **Amazon EventBridge (Event Bus)**.

### EventBridge Bus

- Configured an **EventBridge Event Bus** to act as the central event router.
- This design decouples event producers from consumers, enhancing modularity and scalability.

---

## Phase Two: Rule-Based Filtering in EventBridge

### Event Rules Setup

- Created **EventBridge Rules** to filter events based on specific criteria:
  - **Source Filtering**: Events originating from `com.myapp.orders`.
  - **Detail Filtering**: E.g., `category: "api_gw"`, `category: "sns"` and `category: "step_function"`.
- These filters ensure only relevant events are routed to the appropriate targets.

### API Gateway as a Target

- One of the EventBridge rules forwards matching events back to **API Gateway**, demonstrating dynamic event routing to external systems.

### SQS as a Target

- Added an **SQS queue** as a target to store events for batch processing or manual inspection.

---

## Phase Three: Event Processing and Integration

### Step Functions Workflow

- Designed an **AWS Step Functions** workflow for complex event processing. The workflow includes:
  - **Validation State**: Checks the integrity of the event data.
  - **Enrichment State**: Augments the event with additional metadata.
  - **Categorization State**: Routes the event based on its priority.
  - **Queueing State**: High-priority events are sent to a dedicated queue, while low-priority events trigger notifications or alternative actions.

### SNS as a Target

- Configured an **Amazon SNS** topic as another EventBridge target, enabling notification systems to handle specific events (e.g., sending emails or alerts).

### DynamoDB for Storage

- Integrated **Amazon DynamoDB** to store processed event data for long-term storage and querying.
- Each event is stored with details like `orderId`, `category`, and `amount`.

---

This modular and serverless approach ensures scalability, fault tolerance, and ease of integration across multiple services, making it ideal for modern cloud-native applications.
