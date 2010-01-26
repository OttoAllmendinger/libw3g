rm -r dota_files

mkdir dota_files
(
    cd dota_files
    mpq-extract -e "$1"
)

python extract_mpq.py dota_files
