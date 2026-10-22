// Sealed known violation for CHECK-001's vacuity re-proof.
// If CHECK-001 stops failing on this file, the check has gone vacuous
// and ci_intent_check goes red.
public class RateFetcher
{
    public async Task<string> FetchAsync(string url)
    {
        using var http = new HttpClient();
        return await http.GetStringAsync(url);
    }
}
