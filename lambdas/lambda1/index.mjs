import fetch from 'node-fetch';

export const handler = async (event) => {
  const city = event.queryStringParameters?.city || 'Toronto';
  const apiKey = process.env.OPENWEATHER_API_KEY;

  const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`);
  const data = await response.json();

  return {
    statusCode: 200,
    body: JSON.stringify({
      city: city,
      temperature: data.main?.temp,
      weather: data.weather?.[0]?.description
    })
  };
};

handler()
