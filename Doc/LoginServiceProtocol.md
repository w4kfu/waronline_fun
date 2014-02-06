# Login Service Protocol

WAR.exe at launch will extract XML data from the file *data/mythloginserviceconfig.xml* (data.myp ; Hash name : 0x3FE03665349E2A8C)

The original content is :

    <?xml version="1.0" encoding="utf-8"?>
    <RootElementOfAnyName>
      <MythLoginServiceConfig>
        <Settings>
          <ProductId>2</ProductId>
          <MessageTimeoutSecs>20</MessageTimeoutSecs>
        </Settings>
        <RegionList>
          <Region regionName="WAR Live">
            <PingServer serverName="None">
              <Address>0.0.0.0</Address>
              <Port>0</Port>
            </PingServer>
            <LoginServerList>
              <LoginServer serverName="login 1">
                <Address>107.23.232.189</Address>
                <Port>8046</Port>
              </LoginServer>
              <LoginServer serverName="login 2">
                <Address>107.23.135.143</Address>
                <Port>8046</Port>
              </LoginServer>
            </LoginServerList>
          </Region>
        </RegionList>
      </MythLoginServiceConfig>
    </RootElementOfAnyName>

If you want to be able to manage your own login service, you have to replace
the content of the file inside the data.myp archive, or you can use this
[DLL project][replacexml] that replace the content at runtime.

[replacexml] : https://github.com/w4kfu/waronline_fun/tree/master/Toolz/replace_xml
