var spec = {
    "openapi": "3.0.1",
    "info": {
      "version": "1.0.0",
      "title": "Domains aggregator system"
    },
    "paths": {
      "/domains": {
        "post": {
            "summary": "Save domains clicks",
            "operationId": "saveClicks",
            "tags": [
              "Domains"
            ],
            "requestBody": {
              "content": {
                "application/json": {
                  "schema": {
                    "$ref": "#/components/schemas/Request"
                  }
                }
              }
            },
            "responses": {
              "200": {
                "description": "Success",
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/Response"
                    }
                  }
                }
              },
              "400": {
                "$ref": "#/components/responses/IllegalInput"
              }
            }
          }          
      },
      "/domains/{stats}": {
        "get": {
          "summary": "Get an stats",
          "operationId": "getStats",
          "tags": [
            "Domains"
          ],
          "parameters": [
            {
               "in": "path",
               "name": "stats",
               "required": true,
               "description" : "Statistics type",
               "schema" : {"type" : "string", "enum" : ["min","hour"] }
            }
          ],
          "responses": {
            "200": {
              "description": "Success",
              "content": {
                "application/json": {
                  "schema": {
                    "$ref": "#/components/schemas/stats"
                  }
                }
              }
            },
            "404": {
              "$ref": "#/components/responses/NotFound"
            }
          }
        },
      },      
    }    
};
        