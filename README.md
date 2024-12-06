# Serverless Event-Driven Architecture with AWS SAM

This project demonstrates a **serverless event-driven architecture** using AWS SAM and several AWS services. The goal is to build a highly decoupled and modular system for event processing, showcasing the power of serverless technology.

---

## Workflow Architecture Design

![workflow-design](https://github.com/user-attachments/assets/e4256520-e111-4ec1-a69d-f0de9b8c8733)

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

---

## How Does It Work?

1. **Install SAM CLI**  
   Ensure you have the **AWS SAM CLI** installed on your machine.

2. **Clone the Repository**  
   Download or clone this repository to your local machine.

3. **Deploy the Infrastructure**  
   Open the terminal in the project directory and issue the following command:

`sam deploy --stack-name sam-stack --capabilities CAPABILITY_NAMED_IAM`

The output will provide the API Gateway URL.

4. **Send an Event**  
   Use an HTTP client like Postman and make a `POST` request to the API Gateway URL. Ensure your request includes a valid payload as per the application's requirements.

---

## Verify the Output

Check the respective AWS service consoles to observe the workflow's behavior:

- **Amazon EventBridge**: Monitor the event bus and verify if events are being routed to the correct targets based on the rules.
- **Amazon SQS**: Check the queue to confirm if events are correctly being placed for processing.
- **Amazon DynamoDB**: Review the stored data to ensure events are being stored as expected.

You may choose to switch between different categories (e.g., `api_gw`, `sns`, `step_function`) to test various scenarios and observe how the system handles different types of events.

---

## Clean Up Resources

When you’re done testing or running the workflow, you can remove all provisioned resources with the following command:

`sam delete --stack-name sam-stack`
