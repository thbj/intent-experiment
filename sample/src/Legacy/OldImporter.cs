// Self-test sample: lives under the DEV-001 carve-out (reported
// EXCEPTED, never PASS). Currently conforming anyway.
public class OldImporter
{
    private readonly ApiGateway _gateway;
    public OldImporter(ApiGateway gateway) => _gateway = gateway;
}
