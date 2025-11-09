┌─────────────────────────────────────┐
│ Controller (controllers/)           │
│ - Receives requests                 │
│ - Calls services                    │
│ - Returns response models           │
└─────────────────────────────────────┘
              
┌─────────────────────────────────────┐
│ Service (services/)                 │
│ - Business logic                    │
│ - Orchestrates connectors           │
└─────────────────────────────────────┘
              
┌─────────────────────────────────────┐
│ Response Models (models/responses)  │
│ - JSON structure returned to client │
│ - Pydantic schemas                  │
└─────────────────────────────────────┘