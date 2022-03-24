from omegaconf import OmegaConf


class TestConfig:

    def test_config(self):
        conf = OmegaConf.load('conf/config.yaml')
        s = """
        defaults:
          - _self_
          - cluster: bcm  # Leave it as bcm even if using bcp. It will be ignored for bcp.
          - data_preparation: download_gpt3_pile
          - training: gpt3/5b  # Must match training_config below.
          - conversion: convert_gpt3
          - finetuning: null
          - evaluation: gpt3/evaluate_all
          - override hydra/job_logging: stdout

        hydra:
          run:
            dir: .
          output_subdir: null

        debug: False

        run_data_preparation: True
        run_training: True
        run_conversion: True
        run_finetuning: False # Finetuning only supports T5
        run_evaluation: True

        cluster_type: bcm  # bcm or bcp. If bcm, it must match - cluster above.
        bignlp_path: ???  # Path should end with bignlp-scripts
        data_dir: ${bignlp_path}/data  # Location to store and read the data.
        base_results_dir: ${bignlp_path}/results  # Location to store the results, checkpoints and logs.
        container_mounts: # List of additional paths to mount to container. They will be mounted to same path.
          - null
        container: nvcr.io/ea-bignlp/bignlp-training:22.03-py3

        wandb_api_key_file: null  # File where the w&B api key is stored. Key must be on the first line.
        nccl_topology_xml_file: null  # This file will be exported as "export NCCL_TOPO_FILE=${nccl_topology_xml_file}"

        # Do not modify below, use the values above instead.
        data_config: ${hydra:runtime.choices.data_preparation}
        training_config: ${hydra:runtime.choices.training}
        finetuning_config: ${hydra:runtime.choices.finetuning}
        evaluation_config: ${hydra:runtime.choices.evaluation}
        conversion_config: ${hydra:runtime.choices.conversion}

        # GPU Mapping
        dgxa100_gpu2core:
          0: '48-51,176-179'
          1: '60-63,188-191'
          2: '16-19,144-147'
          3: '28-31,156-159'
          4: '112-115,240-243'
          5: '124-127,252-255'
          6: '80-83,208-211'
          7: '92-95,220-223'

        dgxa100_gpu2mem:
          0: '3'
          1: '3'
          2: '1'
          3: '1'
          4: '7'
          5: '7'
          6: '5'
          7: '5'
        """
        expected = OmegaConf.create(s)
        assert expected == conf, f"conf/config.yaml must be set to {expected} but it currently is {conf}."

