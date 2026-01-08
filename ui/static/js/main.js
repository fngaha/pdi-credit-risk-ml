fetch("/predict", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-TOKEN": window.API_TOKEN || ""
  },
  body: JSON.stringify(payload)
})
