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