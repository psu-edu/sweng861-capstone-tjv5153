const API_URL = "http://localhost:8000";

const ApiFetch = async (endpoint) => {
    try 
    {
        console.log("Making API request to: ", endpoint);
        const response = await fetch(`${API_URL}${endpoint}`, {credentials: 'include'});
        if (!response.ok) 
        {
            if (response.status === 401 || response.status === 403)
            {
                console.log("User is not authenticated. Redirecting to login page...");
                sessionStorage.setItem("authStatus", false);
                window.location.href = "/login";
                return;
            }
            if (response.status === 404)
            {
                console.log("Resource not found.");
            }

            throw new Error(`API request failed: ${response.statusText}`);
        }
        return await response.json();
    } 
    catch (error) 
    {
        console.error("API error:", error);
        throw error;
    }
}

const ApiPost = async (endpoint, data) => {
    console.log("Making API POST request to: ", endpoint, " with data: ", data);
    try 
    {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            credentials: 'include'
        });
        if (!response.ok) 
        {
            throw new Error(`API POST request failed: ${response.statusText}`);
        }
        return await response.json();
    } 
    catch (error) 
    {
        console.error("API POST error:", error);
        throw error;
    }
}

async function GetUserInfo() 
{
    const endpoint = "/userinfo";
    return await ApiFetch(endpoint);
}

async function ApiClientFetch(endpoint) 
{
    return await ApiFetch(endpoint);
}

async function ApiClientPost(endpoint, data) 
{
    return await ApiPost(endpoint, data);
}

async function ApiClientGetUserInfo() 
{
    return await GetUserInfo();
}
export default ApiClientFetch;
export { ApiClientGetUserInfo };
export { ApiClientPost };