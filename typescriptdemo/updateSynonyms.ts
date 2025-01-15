// Import required modules
import * as fs from 'fs'; // File system module for reading and writing files
import * as path from 'path'; // Path module for handling file paths
import * as dotenv from 'dotenv'; // dotenv module to load environment variables
import axios from 'axios'; // HTTP client for making API requests

// Load environment variables from a .env file
dotenv.config();

// Constants for Azure OpenAI API configuration
const OPENAI_API_BASE = process.env.OPENAI_API_BASE || "https://adam-m4ww5pgc-eastus2.openai.azure.com/";
const OPENAI_API_VERSION = process.env.OPENAI_API_VERSION || "v1";
const AZURE_OPENAI_API_KEY = process.env.AZURE_OPENAI_API_KEY || "";

// Log the environment variables to verify they are loaded correctly
console.log("AZURE_OPENAI_API_KEY:", process.env.AZURE_OPENAI_API_KEY);
console.log("OPENAI_API_BASE:", process.env.OPENAI_API_BASE);
console.log("OPENAI_API_VERSION:", process.env.OPENAI_API_VERSION);

// Check if the API key is present, exit if missing
if (!AZURE_OPENAI_API_KEY) {
    console.error("Missing Azure OpenAI API Key.");
    process.exit(1);
}

// Input and output file paths
const inputFile = "NewCLU_Testing.json"; // Path to the input JSON file
const outputFile = "Updated_NewCLU_Testing.json"; // Path to the output JSON file

/**
 * Load JSON file
 * Reads and parses the JSON file from the specified path.
 * @param filePath Path to the file
 * @returns Parsed JSON data
 */
function loadJson(filePath: string): any {
    try {
        const data = fs.readFileSync(filePath, { encoding: 'utf-8' }); // Read file as UTF-8
        console.log(`Loaded JSON file: ${filePath}`);
        return JSON.parse(data); // Parse and return JSON data
    } catch (error) {
        console.error(`Failed to load JSON file ${filePath}:`, error);
        throw error; // Re-throw error for handling
    }
}

/**
 * Save JSON data to a file
 * Writes the JSON data to the specified file path.
 * @param data JSON data to save
 * @param filePath File path to save the data
 */
function saveJson(data: any, filePath: string): void {
    try {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 4), { encoding: 'utf-8' }); // Write JSON with 4-space indentation
        console.log(`Saved updated JSON to: ${filePath}`);
    } catch (error) {
        console.error(`Failed to save JSON file ${filePath}:`, error);
        throw error; // Re-throw error for handling
    }
}

/**
 * Generate synonyms using Azure OpenAI API and clean the result
 * Sends a prompt to the Azure OpenAI API to generate synonyms for the given term.
 * @param listKey Input keyword
 * @returns List of synonyms as strings
 */
async function generateSynonyms(listKey: string): Promise<string[]> {
    const prompt = `List synonyms for the term '${listKey}' as a comma-separated list.`;

    try {
        const response = await axios.post(
            `${OPENAI_API_BASE}/openai/deployments/gpt-4o/chat/completions`, // Azure OpenAI API endpoint
            {
                messages: [
                    { role: "system", content: "You are a helpful assistant that provides a clean, comma-separated list of synonyms for given terms." },
                    { role: "user", content: prompt }
                ],
                max_tokens: 50, // Limit the response to 50 tokens
                temperature: 0.5, // Controls randomness of the response
                top_p: 0.9, // Nucleus sampling parameter
                frequency_penalty: 0, // Reduces repetitive text
                presence_penalty: 0, // Controls topic relevance
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'api-key': AZURE_OPENAI_API_KEY // API key for authentication
                },
                params: {
                    "api-version": OPENAI_API_VERSION // API version
                }
            }
        );

        // Extract the content of the response
        const synonymsContent = response.data.choices[0].message.content;

        // Use regex to extract clean words or phrases and remove unnecessary text
        const synonyms = synonymsContent.match(/\b[a-zA-Z\s-]+\b/g) || [];
        return Array.from(new Set(synonyms.map(syn => syn.trim()))); // Remove duplicates and trim whitespace
    } catch (error) {
        console.error(`Error while generating synonyms for '${listKey}':`, error);
        return []; // Return an empty list in case of an error
    }
}

/**
 * Update synonyms in the JSON data
 * Iterates through the entities and updates their synonyms using the Azure OpenAI API.
 * @param data Original JSON data
 * @returns Updated JSON data
 */
async function updateSynonyms(data: any): Promise<any> {
    const entities = data.assets?.entities || []; // Retrieve entities from the JSON data

    for (const entity of entities) {
        const sublists = entity.list?.sublists || []; // Retrieve sublists from the entity

        for (const sublist of sublists) {
            const listKey = sublist.listKey; // Retrieve the list key
            if (listKey) {
                await new Promise(resolve => setTimeout(resolve, 10000)); // Delay 10 seconds between requests

                const synonyms = await generateSynonyms(listKey); // Generate synonyms
                for (const synonymEntry of sublist.synonyms || []) {
                    if (synonymEntry.language === "en-us") { // Update only English synonyms
                        const existingValues = synonymEntry.values || []; // Retrieve existing synonym values
                        synonymEntry.values = Array.from(new Set([...existingValues, ...synonyms])); // Merge and remove duplicates
                        console.log(`Updated synonyms for listKey '${listKey}':`, synonymEntry.values);
                    }
                }
            }
        }
    }

    return data; // Return the updated JSON data
}

/**
 * Main function
 * Coordinates loading JSON, updating synonyms, and saving the updated data.
 */
(async function main() {
    try {
        // Load JSON data from the input file
        const data = loadJson(inputFile);

        // Update synonyms in the JSON data
        const updatedData = await updateSynonyms(data);

        // Save the updated JSON data to the output file
        saveJson(updatedData, outputFile);

        console.log("Synonyms have been added and the file has been updated successfully.");
    } catch (error) {
        console.error("An error occurred during processing:", error);
    }
})();
