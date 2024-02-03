cd /data-nfs/AIDA/papers_v4/

unzip papers_v2.zip

cd papers_v4/

head -n 17 papers_0.ttl >> declaration.ttl

mkdir all_ttl

mv papers_*.ttl all_ttl/

cd all_ttl/

# remove the declaration from each ttl file
for file in *.ttl; do                             
tail -n +18 "$file" > "temp_$file" && mv "temp_$file" "$file"; done

cat ../declaration.ttl papers_* > all.ttl

grep '@prefix' all.ttl | wc -l
# which should return 17