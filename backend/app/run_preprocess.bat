python data_loading_db.py -c configs/challengers.json
python data_loading_db.py -c configs/grandmasters.json
python team_composition.py -c configs/challengers.json
python team_composition.py -c configs/grandmasters.json
python optimizer.py -c configs/config_xgb.json