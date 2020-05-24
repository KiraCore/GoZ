# Query Hub Winners

gaiacli query ibc client states --chain-id gameofzoneshub-1b -o json --limit 1500 | jq ' .[] | select(.value.trusting_period!=null) | (.value.trusting_period +","+.value.last_header.signed_header.header.time+","+.value.last_header.signed_header.header.chain_id  )'


# Phase 1b
> Liveness Reward

docker exec -it $(docker ps -a -q --filter ancestor=kiracore/goz:kira-goz-relayer) bash


cat $SELF_UPDATE/common/configs/kira-1-2-long.json > a.json 
cat $SELF_UPDATE/common/configs/goz-hub-long.json > b.json
cat $SELF_UPDATE/common/configs/kira-alpha.json > b.json # optionally

cat a.json
cat b.json

m="cost goat lazy genre spring transfer uncle canvas fashion tuition tired heart usual child gauge flag sign barrel during disagree false ocean drum weekend" && \
 j1=./a.json && \
 j2=./b.json && \
 i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 k=long && \
 p="${s}_${d}_long"

echo $p

rly ch d $s && rly ch d $d && \
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k d $s $k$s ||: && rly k d $d $k$d ||: && \
 rly k r $s $k$s "$m" && rly k r $d $k$d "$m" && \
 rly ch e $s key $k$s && rly ch e $d key $k$d && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 rly tst req $s || : && rly tst req $d || :

rly q bal $s -j
rly q bal $d -j

rly tx clnts $p -d
rly tx conn $p -d
rly tx chan $p -d

rly pth s $p && sp=$(rly pth s $p -j) && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \
 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq)

echo "Time Source: $ts"
echo "Time Destin: $td"

rly tx raw uc $d $s $dc
rly tx raw uc $s $d $sc

#Check time again

# check balances


`##################################################################################`
`# OUTPUT`
`##################################################################################`

# cat a.json
{
  "key": "faucet",
  "chain-id": "kira-1-1b",
  "rpc-addr": "http://internal-goz.kiraex.com:10001",
  "account-prefix": "cosmos",
  "gas": 200000,
  "gas-min": 70000,
  "gas-step": 10000,
  "gas-max": 2000000,
  "gas-prices": "0.0025ukex",
  "default-denom": "ukex",
  "trusting-period": "100h"
}
# cat b.json
{
  "key": "faucet",
  "chain-id": "gameofzoneshub-1b",
  "rpc-addr": "http://goz-trust-alias.kiraex.com:26657",
  "account-prefix": "cosmos",
  "gas": 200000,
  "gas-min": 70000,
  "gas-step": 5000,
  "gas-max": 2000000,
  "gas-prices": "0.0025doubloons",
  "default-denom": "doubloons",
  "trusting-period": "100h"
}

# echo $p
kira-1-1b_gameofzoneshub-1b_long

Error: a key with name longkira-1-1b doesn't exist
a key with name longkira-1-1b doesn't exist
Error: a key with name longgameofzoneshub-1b doesn't exist
a key with name longgameofzoneshub-1b doesn't exist
cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c
cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c
Error: path with name kira-1-1b_gameofzoneshub-1b_long does not exist
path with name kira-1-1b_gameofzoneshub-1b_long does not exist
{"address":"cosmos1efzs6x9244z9hjz6pcrsam4muxxms74wz98h7c","amount":"200000000ukex"}
Error: Post "http://goz-trust-alias.kiraex.com:8000": dial tcp 10.128.0.59:8000: connect: connection refused
Post "http://goz-trust-alias.kiraex.com:8000": dial tcp 10.128.0.59:8000: connect: connection refused

# rly q bal $s -j
[{"denom":"ukex","amount":"200000000"}]
# rly q bal $d -j
[{"denom":"doubloons","amount":"1200000"}]

# rly tx clnts $p -d
I[2020-05-18|00:25:20.539] - [kira-1-1b] -> creating client for [gameofzoneshub-1b]header-height{48452} trust-period(100h0m0s) 
I[2020-05-18|00:25:20.565] - [gameofzoneshub-1b] -> creating client for [kira-1-1b]header-height{3486} trust-period(100h0m0s) 
I[2020-05-18|00:25:22.385] ✔ [kira-1-1b]@{3487} - msg(0:create_client) hash(33FE74A89385361AC2E0E02F7B81ED34613E14D718825A5876AD94A7D3363BF3) 
I[2020-05-18|00:25:25.306] ✔ [gameofzoneshub-1b]@{48453} - msg(0:create_client) hash(40D4339F8C89F40B0C9017D87F31BA9CD285C3017DAE170B18516F3D5BF1CCD4) 
I[2020-05-18|00:25:25.307] ★ Clients created: [kira-1-1b]client(kencdqzctf) and [gameofzoneshub-1b]client(etwwrivwuz) 

# rly tx conn $p -d
I[2020-05-18|00:25:56.366] - [kira-1-1b]@{0}conn(ahkhilfgsp)-{STATE_UNINITIALIZED_UNSPECIFIED} : [gameofzoneshub-1b]@{0}conn(pfuqeppgbd)-{STATE_UNINITIALIZED_UNSPECIFIED} 
I[2020-05-18|00:25:57.599] ✔ [kira-1-1b]@{3494} - msg(0:connection_open_init) hash(FC4E55ECDB9B039BF8A0730FACE3E94BD255279125D0B54D55801292BF3F4F0A) 
I[2020-05-18|00:26:06.364] - [gameofzoneshub-1b]@{0}conn(pfuqeppgbd)-{STATE_UNINITIALIZED_UNSPECIFIED} : [kira-1-1b]@{3494}conn(ahkhilfgsp)-{STATE_INIT} 
I[2020-05-18|00:26:07.929] ✔ [gameofzoneshub-1b]@{48461} - msg(0:update_client,1:connection_open_try) hash(6D53FFC03CB7169E055AB428921102CA1749B00B2E0A72AB7F32B5C7E34A5E97) 
I[2020-05-18|00:26:16.360] - [kira-1-1b]@{3496}conn(ahkhilfgsp)-{STATE_INIT} : [gameofzoneshub-1b]@{48461}conn(pfuqeppgbd)-{STATE_TRYOPEN} 
I[2020-05-18|00:26:17.710] ✔ [kira-1-1b]@{3498} - msg(0:update_client,1:connection_open_ack) hash(032CECB08BBAA19FD1F3940BFA6D314DC361CE9BD7FE8557E3684A8759160027) 
I[2020-05-18|00:26:26.385] - [gameofzoneshub-1b]@{48463}conn(pfuqeppgbd)-{STATE_TRYOPEN} : [kira-1-1b]@{3498}conn(ahkhilfgsp)-{STATE_OPEN} 
I[2020-05-18|00:26:29.201] ✔ [gameofzoneshub-1b]@{48465} - msg(0:update_client,1:connection_open_confirm) hash(DCF813F200F106526AFCAB9E1D813A9C143048231300F01FB765DA26E468AF27) 
I[2020-05-18|00:26:29.204] - [kira-1-1b]@{3500}conn(ahkhilfgsp)-{STATE_OPEN} : [gameofzoneshub-1b]@{48465}conn(pfuqeppgbd)-{STATE_OPEN} 
I[2020-05-18|00:26:29.204] ★ Connection created: [kira-1-1b]client{kencdqzctf}conn{ahkhilfgsp} -> [gameofzoneshub-1b]client{etwwrivwuz}conn{pfuqeppgbd} 

# rly tx chan $p -d
I[2020-05-18|00:26:57.553] - [kira-1-1b]@{0}chan(bngangchya)-{STATE_UNINITIALIZED_UNSPECIFIED} : [gameofzoneshub-1b]@{0}chan(xqdgmttdgz)-{STATE_UNINITIALIZED_UNSPECIFIED} 
I[2020-05-18|00:26:57.937] ✔ [kira-1-1b]@{3506} - msg(0:channel_open_init) hash(FDB57B8CF2C27D475F3F511EF655991756D3B5F83AA8349218692C2EC3A79C39) 
I[2020-05-18|00:27:07.531] - [gameofzoneshub-1b]@{0}chan(xqdgmttdgz)-{STATE_UNINITIALIZED_UNSPECIFIED} : [kira-1-1b]@{3506}chan(bngangchya)-{STATE_INIT} 
I[2020-05-18|00:27:11.914] ✔ [gameofzoneshub-1b]@{48473} - msg(0:update_client,1:channel_open_try) hash(7E15E8608CF057465BCB9F84EED918831F152CEC5D2FE57C01B06B523BA6BA9C) 
I[2020-05-18|00:27:17.523] - [kira-1-1b]@{3508}chan(bngangchya)-{STATE_INIT} : [gameofzoneshub-1b]@{48473}chan(xqdgmttdgz)-{STATE_TRYOPEN} 
I[2020-05-18|00:27:18.046] ✔ [kira-1-1b]@{3510} - msg(0:update_client,1:channel_open_ack) hash(4F757405D08A93083F4995C4FABDEA83C40BDCB3DC695ABD5A4721E6659A3CB2) 
I[2020-05-18|00:27:27.570] - [gameofzoneshub-1b]@{48474}chan(xqdgmttdgz)-{STATE_TRYOPEN} : [kira-1-1b]@{3510}chan(bngangchya)-{STATE_OPEN} 
I[2020-05-18|00:27:33.255] ✔ [gameofzoneshub-1b]@{48477} - msg(0:update_client,1:channel_open_confirm) hash(8CF04B45D9CDE8CE2C58CC5AB5D17AE7CBC9C1EFF20E3C8825D68F16E6F7727B) 
I[2020-05-18|00:27:33.257] - [kira-1-1b]@{3513}chan(bngangchya)-{STATE_OPEN} : [gameofzoneshub-1b]@{48477}chan(xqdgmttdgz)-{STATE_OPEN} 
I[2020-05-18|00:27:33.258] ★ Channel created: [kira-1-1b]chan{bngangchya}port{transfer} -> [gameofzoneshub-1b]chan{xqdgmttdgz}port{transfer} 

Path "kira-1-1b_gameofzoneshub-1b_long" strategy(naive):
  SRC(kira-1-1b)
    ClientID:     kencdqzctf
    ConnectionID: ahkhilfgsp
    ChannelID:    bngangchya
    PortID:       transfer
  DST(gameofzoneshub-1b)
    ClientID:     etwwrivwuz
    ConnectionID: pfuqeppgbd
    ChannelID:    xqdgmttdgz
    PortID:       transfer
  STATUS:
    Chains:       ✔
    Clients:      ✔
    Connection:   ✔
    Channel:      ✔

# echo "Time Source: $ts"
Time Source: 2020-05-18T00:27:11.561754989Z
# echo "Time Destin: $td"
Time Destin: 2020-05-18T00:27:18.028023853Z

# rly q bal $s -j
[{"denom":"ukex","amount":"199997500"}]
# rly q bal $d -j
[{"denom":"doubloons","amount":"1197500"}]

> Connection Cost: `2500`

# rly tx raw uc $d $s $dc
{"height":"48516","txhash":"509D02114AB690AEC41C6269FF850D94370002AD1D0774D2600D6BDFD683DF9A","logs":[{"msg_index":0,"log":"","events":[{"type":"message","attributes":[{"key":"action","value":"update_client"}]}]}],"gas_wanted":"200000","gas_used":"84318"}

# rly tx raw uc $s $d $sc
{"height":"3560","txhash":"7ED5B7A3928FDBF67B1C03B0081D240C28E9A3FEA31404E84324E8CC4C92AA82","logs":[{"msg_index":0,"log":"","events":[{"type":"message","attributes":[{"key":"action","value":"update_client"}]}]}],"gas_wanted":"200000","gas_used":"111247"}

# rly q bal $s -j
[{"denom":"ukex","amount":"199997000"}]

# rly q bal $d -j
[{"denom":"doubloons","amount":"1197000"}]

> Update Cost: `500`








`##################################################################################`

# phase 2
cat $SELF_UPDATE/common/configs/kira-1-1b.json > kira-1-1b.json 
cat $SELF_UPDATE/common/configs/kira-alpha.json > kira-alpha.json
cat $SELF_UPDATE/common/configs/goz-hub.json > goz-hub.json

m="cost goat lazy genre spring transfer uncle canvas fashion tuition tired heart usual child gauge flag sign barrel during disagree false ocean drum weekend" && \
 j1=./kira-alpha.json && \
 j2=./kira-1-1b.json && \
 k=alpha

i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 p="$s_$d" && \
 rly ch d $s && rly ch d $d && \
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k d $s $k$s ||: && rly k d $d $k$d ||: && \
 rly k r $s $k$s "$m" && rly k r $d $k$d "$m" && \
 rly ch e $s key $k$s && rly ch e $d key $k$d && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 rly tst req $s || : && rly tst req $d || : && \
 rly q bal $s -j && rly q bal $d -j && \
 rly tx clnts $p -d &> clnts.log; wait && \
 rly tx conn $p -d &> conn.log; wait && \
 rly tx chan $p -d &> chan.log; wait && \
 rly pth s $p && sp=$(rly pth s $p -j) && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \
 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
 echo "Time Source: $ts" && echo "Time Destin: $td" && \
 while :; do \
  rly pth s $p && sp=$(rly pth s $p -j) && \
  rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc && \
  dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
  sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
  tq=".client_state.value.last_header.signed_header.header.time" && \
  ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
  echo "Time Source: $ts" && echo "Time Destin: $td" && \
  echo "SUCCESS" && rly q bal $s -j && rly q bal $d -j && sleep 5300 ; done




# rly ch edit $s gas 50000
# rly ch edit $s gas 50000 && rly transact raw update-client $s $d $(rly pth s $p -j | jq -r '.chains.src."client-id"')
# rly q unrelayed $p
# rly tx rly $p --debug
# rly q bal $s -j

# price=90000 && rly ch edit $s gas $price 

# price=90000 && rly ch edit $s gas $price &&  rly ch edit $d gas $price && rly tx transfer $s $d 1ukex true $(rly ch addr $s) -d
# price=90000 && rly ch edit $s gas $price &&  rly ch edit $d gas $price && rly tx transfer $s $d 1ukex true $(rly ch addr $s) -d




CDHelper email send \
 --from="noreply@kiracore.com" \
 --to="asmodat@gmail.com" \
 --subject="[GoZ] $(curl -H 'Metadata-Flavor: Google' http://metadata/computeMetadata/v1/instance/name 2>/dev/null) DEBUG" \
 --body="[$(date)] PHASE1 debug." \
 --html="false" \
 --recursive="false" \
 --attachments="$SELF_LOGS/relayer.txt"
    exit 1




# Usefully Snippets
```
cat $SELF_UPDATE/common/configs/kira-1.json > kira-1.json 
cat $SELF_UPDATE/common/configs/kira-alpha.json > kira-alpha.json
cat $SELF_UPDATE/common/configs/goz-hub.json > goz-hub.json

m=$RLYKEY_MNEMONIC && \
 j1=./kira-1-1b.json && \
 j2=./goz-hub.json

m="cost goat lazy genre spring transfer uncle canvas fashion tuition tired heart usual child gauge flag sign barrel during disagree false ocean drum weekend" && \
 j1=./kira-alpha.json && \
 j2=./kira-1-1b.json

i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 p="$s-$d" && \
 rly ch d $s && rly ch d $d && \
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k d $s k$s ||: && rly k d $d k$d ||: && \
 rly k r $s k$s "$m" && rly k r $d k$d "$m" && \
 rly ch e $s key k$s && rly ch e $d key k$d && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 rly tst req $s || : && rly tst req $d || : && \
 rly q bal $s -j && rly q bal $d -j && \
 rly tx clnts $p -d &> clnts.log; wait && \
 rly tx conn $p -d &> conn.log; wait && \
 rly tx chan $p -d &> chan.log; wait && \
 rly pth s $p && sp=$(rly pth s $p -j) && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \
 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
 echo "Time Source: $ts" && echo "Time Destin: $td" && \
 while :; do \
  rly pth s $p && sp=$(rly pth s $p -j) && \
  rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc && \
  dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
  sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
  tq=".client_state.value.last_header.signed_header.header.time" && \
  ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
  echo "Time Source: $ts" && echo "Time Destin: $td" && \
  echo "SUCCESS" && rly q bal $s -j && rly q bal $d -j && sleep 5300 ; done

rly dev goz-dump kira-1
rly dev goz-dump gameofzoneshub-1a
rly q unrelayed kira-1_gameofzoneshub-1a
rly tx rly kira-1_gameofzoneshub-1a

m="your memo words come ... here" && j1=./your-node.json && j2=./goz-hub.json && i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && p="$s-$d" && rly ch d $s && rly ch d $d && rly ch a -f $j1 && rly ch a -f $j2 && rly k d $s k$s ||: && rly k d $d k$d ||: && rly k r $s k$s "$m" && rly k r $d k$d "$m" && rly ch e $s key k$s && rly ch e $d key k$d && rly l d $s && rly l d $d && rly pth d $p || : && rly pth gen $s transfer $d transfer $p -f && rly l i $s -f && rly l i $d -f && rly l u $s && rly l u $d && rly tst req $s || : && rly tst req $d || : && rly q bal $s -j && rly q bal $d -j && rly tx clnts $p -d &> clnts.log; wait && rly tx conn $p -d &> conn.log; wait && rly tx chan $p -d &> chan.log; wait && rly pth s $p && dc=$(rly pth s $p -j | jq -r '.chains.dst."client-id"') && sc=$(rly pth s $p -j | jq -r '.chains.src."client-id"') && while :; do rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc && sleep 5300 ; done
 ```

:26657/status

`rly k d $s k$s && rly ch d $s && rly ch a -f $j1 && rly k r $s k$s "$m" && rly ch e $s key k$s && rly ch list $s && rly q bal $s`


i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 p="$s-$d" && \
 
 rly k d $s k$s ||: && rly k d $d k$d ||: && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly ch d $s && rly ch d $d && \
 
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k r $s k$s "$m" && rly k r $d k$d "$m" && \
 rly ch e $s key k$s && rly ch e $d key k$d && \
 rly tst req $s || : && rly tst req $d || : && \
 rly q bal $s -j && rly q bal $d -j && \

 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 
 rly tx clnts $p -d &> clnts.log; wait && \
 rly tx conn $p -d &> conn.log; wait && \
 rly tx chan $p -d &> chan.log; wait && \
 rly pth s $p && sp=$(rly pth s $p -j) && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \

 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
 echo "Time Source: $ts" && echo "Time Destin: $td" && \

 while :; do rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc && echo "SUCCESS" && rly q bal $s -j && rly q bal $d -j && sleep 5300 ; done

> Check for last updated time
Last header: `echo $(rly q client $s $sc | jq -r '.client_state.value.last_header.signed_header.header.time') `



i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 p="$s-$d" && \
 rly ch d $s && rly ch d $d && \
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k d $s k$s ||: && rly k d $d k$d ||: && \
 rly k r $s k$s "$m" && rly k r $d k$d "$m" && \
 rly ch e $s key k$s && rly ch e $d key k$d && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 rly tst req $s || : && rly tst req $d || : && \
 rly q bal $s -j && rly q bal $d -j && \
 rly tx clnts $p -d &> clnts.log; wait && \
 rly tx conn $p -d &> conn.log; wait && \
 rly tx chan $p -d &> chan.log; wait && \
 rly pth s $p && sp=$(rly pth s $p -j) && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \
 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
 echo "Time Source: $ts" && echo "Time Destin: $td" && \
 rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc


Time Source: 2020-05-08T04:25:27.715616164Z
Time Destin: 2020-05-08T04:25:33.524691684Z

i=$(cat $j1) && s=$(echo $i | jq -r '."chain-id"') && \
 o=$(cat $j2) && d=$(echo $o | jq -r '."chain-id"') && \
 p="$s-$d" && \
 rly ch d $s && rly ch d $d && \
 rly ch a -f $j1 && rly ch a -f $j2 && \
 rly k d $s k$s ||: && rly k d $d k$d ||: && \
 rly k r $s k$s "$m" && rly k r $d k$d "$m" && \
 rly ch e $s key k$s && rly ch e $d key k$d && \
 rly l d $s && rly l d $d && rly pth d $p || : && \
 rly pth gen $s transfer $d transfer $p -f && \
 rly l i $s -f && rly l i $d -f && \
 rly l u $s && rly l u $d && \
 rly tst req $s || : && rly tst req $d || : && \
 rly q bal $s -j && rly q bal $d -j && \
 rly tx clnts $p -d &> clnts.log; wait && \
 rly tx conn $p -d &> conn.log; wait && \
 rly tx chan $p -d &> chan.log; wait && \
 rly pth s $p && sp=$(rly pth s $p -j) && echo $sp > p && \
 dc=$(echo $sp | jq -r '.chains.dst."client-id"') && \
 sc=$(echo $sp | jq -r '.chains.src."client-id"') && \
 dh=$(echo $sp | jq -r '.chains.dst."channel-id"') && \
 sh=$(echo $sp | jq -r '.chains.src."channel-id"') && \
 dn=$(echo $sp | jq -r '.chains.dst."connection-id"') && \
 sn=$(echo $sp | jq -r '.chains.src."connection-id"') && \
 tq=".client_state.value.last_header.signed_header.header.time" && \
 ts=$(rly q client $s $sc | jq -r $tq) && td=$(rly q client $d $dc | jq -r $tq) && \
 echo "Time Source: $ts" && echo "Time Destin: $td" && \
 rly tx raw uc $d $s $dc && rly tx raw uc $s $d $sc

 ```
rly pth s $p -j > p
 ```

rly pth add $s $d $p --file ./p