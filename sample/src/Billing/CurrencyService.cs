// Self-test sample: conforming code — uses the gateway.
public class CurrencyService
{
    private readonly ApiGateway _gateway;
    public CurrencyService(ApiGateway gateway) => _gateway = gateway;

    public async Task<decimal> GetRateAsync(string currency) =>
        await _gateway.GetAsync<decimal>($"/rates/{currency}");
}
