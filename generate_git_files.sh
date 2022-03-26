HASH=$(git show --pretty='format:%H' HEAD | head -1)
UPSTREAM=$(git remote get-url origin)
DIRNAME=$(basename $UPSTREAM '.git')

cat > download_update.sh << EOF
## GENERATED FILE, DO NOT MODIFY

# Utility methods
function do_cleanup() {
    if [[ -f /staging/$DIRNAME ]]
    then
        rm -rf /staging/$DIRNAME
    fi
}

# Start with cleanup
do_cleanup

# Clone the repository
mkdir -p /staging
cd /staging
git clone $UPSTREAM
cd $DIRNAME
git pull

# Check if update needed. If not, clean up and exit
# the script
NEW_HASH=\$(git show --pretty='format:%H' HEAD | head -1)
if [[ '$HASH' == \$NEW_HASH ]]
then
    do_cleanup
    exit 0
fi

# Install the new version of the thermostat
./install.sh
INSTALL_RESULT=\$?

# Clean up and return
do_cleanup
exit \$INSTALL_RESULT

EOF
chmod +x download_update.sh

cat > management_service/build_info.py << EOF
## GENERATED FILE, DO NOT MODIFY

import json
from main import app

BUILD_VER = '$HASH'

@app.route('/build_info')
def buildInfo():
    return json.dumps({
        "ver": BUILD_VER
    })

EOF

cat > update_service/git_info.py << EOF
## GENERATED FILE, DO NOT MODIFY

GIT_ORIGIN = '$UPSTREAM'

EOF

cat > user_interface/git_info.js << EOF
// GENERATED FILE, DO NOT MODIFY

const BUILD_VER = '$HASH'

EOF
