from engine.integrations.services.provider.provider import Provider


if not __name__ == "__main__":
    provider = Provider()
    result = provider.getDeployment("sample", "")
    print(result)


if not __name__ == "__main__":
    provider = Provider()
    result = provider.getDeployments("", "")
    print(result)


if __name__ == "__main__":
    provider = Provider()
    result = provider.createDeployment(
        "sample", "rounak316/dsad", "6033fa965b22581da55edb70")
    print(result)


# result = CreateJob( "test_tool",  "rounak316/dsad", "6033fa965b22581da55edb70")
# print(result)
