export tnm=frag5-dfmp2-grad
export mem=16GB

uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n2.out -n2 --memory=$mem
uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n4.out -n4 --memory=$mem
uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n6.out -n6 --memory=$mem
uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n8.out -n8 --memory=$mem
uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n10.out -n10 --memory=$mem
uptime
time psi4 --qcschema $tnm.json -o $tnm.json.n1.out -n1 --memory=$mem


#nohup ./runem.sh > runem.log 2>&1 < /dev/null &
#disown
