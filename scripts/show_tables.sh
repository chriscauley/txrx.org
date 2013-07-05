DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
psql --username=postgres txrx <$DIR/_show_tables.sql