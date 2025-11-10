import axios from 'axios'

if (process.env.EXPO_PUBLIC_APP_ENV !== 'dev' &&
    process.env.EXPO_PUBLIC_APP_ENV !== 'prod'
) {
    throw new Error("EXPO_PUBLIC_APP_ENV should be set to either 'dev' or 'prod' explicitly")
}

const baseURL = process.env.EXPO_PUBLIC_APP_ENV === 'dev' ?
    'http://localhost:8000/' :
    'https://api.my-pregnancy.click/'

// Please use this instance for all your API calls
export const api = axios.create({
    baseURL: baseURL
})