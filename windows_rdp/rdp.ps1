echo "Connecting to 192.168.1.100"
$Server="3.95.153.32"
$User="Administrator"
$Password="g)!xOCfxpB%PUnp7(D6)8.isUSz*-b&P"
cmdkey /generic:TERMSRV/$Server /user:$User /pass:$Password
mstsc /v:$Server