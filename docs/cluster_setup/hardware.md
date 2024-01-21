# Hardware

A cluster is a collection of single-board computers connected together to form a distributed computing system. In this section, we will create a simple cluster of micro-ARM devices with multiple nodes, typically used for educational purposes, testing, or small-scale distributed computing experiments.

## Shopping cart

This is the list of hardware needed in order to setup a Kubernetes cluster with enough cpu and memory capacity for our needs:

| Name                                                       | Link                                                                                                            |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| 1x Raspberri Pi 3 or later (2 GB Ram or better)            | I reuse an old one.                                                                                             |
| >3x OrangePi 5 with >=16 GB Ram.                           | In my case I will use **OrangePi 5 model B** which includes internal storage.                                   |
|                                                            | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005057630718.html)                                    |
| Case + Fan for all devices                                 | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005057630718.html)                                    |
| 4x 64 GB microSDXC card (Samsung EVO Plus MicroSDXC 64 GB) | [:simple-amazon: link](https://www.amazon.com/SAMSUNG-microSDXC-Expanded-MB-MC64KA-AM/dp/B09THJ25JR/)                |
| 3x NVME 256GB SSD (if using OrangePi model 5 or 5+)        | [:simple-amazon: link](https://www.amazon.com/Kingston-250G-2280-Internal-SNV2S/dp/B0BBWH7DBT/)                      |
| 4x very short LAN CAT6 cable                               | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005006102502476.html)                                    |
| 4x very short HDMI cable                                   | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005003995751089.html)                                    |
| 4x very short USB type C cables                            | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005058400078.html)                                    |
| Gigabit Switch 8 Ports                                     | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005315707615.html)                                    |
| M3 Circuit Boards Spacer screws                            | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005002907172267.html)                                    |
| HDMI Splitter 5x1                                          | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005905850399.html)                                    |
| +200W power supply Splitter 5x1                            | [:simple-amazon: link](https://www.amazon.com/Aluminum-Charger-Charging-Station-Compatible/dp/B0BFN6JKMV/ref=sr_1_5) |
| Mini PC case                                               | [:simple-amazon: link](https://www.amazon.es/dp/B0CGV9Q3VP)                                                          |
| PC Chassis Cooling Dust Mesh                               | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005005677590985.html)                                    |
| RJ45 female-female connector                               | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005002947244816.html)                                    |
| HDMI female-female connector                               | [:simple-aliexpress: link](https://www.aliexpress.com/item/1005002946714841.html)                                    |

## Montage

- **Step 1: Assemble ARM devices Cluster**
- **Step 2: Simple Connect and Test**
- **Step 3: Assemble components in PC Case**
- **Step 4: Final Test**

## OS setup

- **Step 1: Download and Install Raspbian OS**
- **Step 2: Initial Configuration**
- **Step 3: Connectivity Test**