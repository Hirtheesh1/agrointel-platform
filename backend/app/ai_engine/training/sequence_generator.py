from pytorch_forecasting import TimeSeriesDataSet
from app.ai_engine.training.hyperparameter_config import tft_config

class SequenceGenerator:
    """
    Converts dataframes into TimeSeriesDataSet objects for TFT.
    """
    
    def create_dataset(self, df, is_training: bool = True, train_dataset: TimeSeriesDataSet = None) -> TimeSeriesDataSet:
        """
        Creates a TimeSeriesDataSet from a dataframe.
        """
        if not is_training and train_dataset is not None:
            return TimeSeriesDataSet.from_dataset(train_dataset, df, predict=False, stop_randomization=True)
            
        return TimeSeriesDataSet(
            df,
            time_idx="time_idx",
            target=tft_config.target,
            group_ids=tft_config.group_ids,
            min_encoder_length=tft_config.max_encoder_length // 2,
            max_encoder_length=tft_config.max_encoder_length,
            min_prediction_length=1,
            max_prediction_length=tft_config.max_prediction_length,
            static_categoricals=["farm_id"],
            time_varying_known_reals=["time_idx", "hour_of_day", "day_of_week", "month_of_year"],
            time_varying_unknown_reals=[
                "temperature", "humidity", "rainfall", "wind_speed", 
                "temperature_lag_1", "humidity_lag_1", "rainfall_lag_1"
            ],
            target_normalizer=None,  # Use default or scaling
            add_relative_time_idx=True,
            add_target_scales=True,
            add_encoder_length=True,
            allow_missing_timesteps=True
        )

sequence_generator = SequenceGenerator()
