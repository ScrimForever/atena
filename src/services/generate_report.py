import pprint
from dataclasses import dataclass
import os
from utils.settings_config import settings
import json
from collections import defaultdict


@dataclass
class GenerateReport:


    def _total_order_by_customer(self, merged: list):
        orders_per_customer = defaultdict(int)
        customer_ids_by_name = defaultdict(set)

        for item in merged:
            customer_id = item['id']
            customer_name = item['name']
            customer_ids_by_name[customer_name].add(customer_id)
            orders_per_customer[customer_name] += 1

        content = {}
        for customer_name in sorted(orders_per_customer.keys()):
            order_count = orders_per_customer[customer_name]
            customer_ids = sorted(customer_ids_by_name[customer_name])
            ids_str = ", ".join(map(str, customer_ids))
            print(f"{customer_name} (ID: {ids_str}) {order_count} pedido(s)")
            content[customer_name] = {
                "ID": ids_str,
                "order_count": order_count
            }
        return {
            "customers": content
        }

    def _total_by_contry(self, merged: list, mount_dict: dict):
        revenue_per_country = defaultdict(float)

        for item in merged:
            country = item['country']
            order_value = item['quantity'] * item['price']
            revenue_per_country[country] += order_value


        dict_country = {}
        for country in sorted(revenue_per_country.keys()):
            revenue = revenue_per_country[country]
            print(f"{country:20}: R$ {revenue:,.2f}")
            dict_country[country] = revenue

        total_revenue = sum(revenue_per_country.values())
        print(f"{'TOTAL':20}: R$ {total_revenue:,.2f}")
        dict_country["total"] = total_revenue
        mount_dict.update({"country": dict_country})
        x = mount_dict
        return x

    def _total_by_quantity(self, merged: list, mount_dict: dict):
        print(mount_dict)
        quantity_per_product = defaultdict(int)
        product_revenue = defaultdict(float)

        for item in merged:
            product = item['product']
            quantity = item['quantity']
            price = item['price']
            quantity_per_product[product] += quantity
            product_revenue[product] += quantity * price

        sorted_products = sorted(quantity_per_product.items(), key=lambda x: x[1], reverse=True)
        dict_revenue = {}
        for product, quantity in sorted_products:
            revenue = product_revenue[product]
            print(f"{product:<20} {quantity:>12} R$ {revenue:>18,.2f}")
            best_product = sorted_products[0]
            dict_revenue[product] = {
                "quantity": quantity,
                "revenue": revenue
            }
        print(f"Product (best seller): {best_product[0]} ({best_product[1]} unidades)")
        dict_revenue["best_seller"] = best_product[0]
        mount_dict.update({"Products": dict_revenue})
        x = mount_dict
        pprint.pprint(x)
        return x



    def _total_by_spending(self, merged: list, mount_dict):
        spending_per_customer = defaultdict(float)
        customer_orders = defaultdict(list)
        customer_countries = {}

        for item in merged:
            customer_name = item['name']
            country = item['country']
            order_value = item['quantity'] * item['price']
            spending_per_customer[customer_name] += order_value
            customer_countries[customer_name] = country
            customer_orders[customer_name].append({
                'product': item['product'],
                'quantity': item['quantity'],
                'price': item['price'],
                'order_value': order_value
            })



        sorted_customers = sorted(spending_per_customer.items(), key=lambda x: x[1], reverse=True)
        dict_spending = {}
        for customer_name, total_spent in sorted_customers:
            country = customer_countries[customer_name]
            num_orders = len(customer_orders[customer_name])
            print(f"{customer_name:<15} {country:<15} R$ {total_spent:>18,.2f} {num_orders:>12}")
            dict_spending[customer_name] = {
                "country": country,
                "total_spent": total_spent,
                "orders": num_orders
            }


        top_customer = sorted_customers[0]
        top_customer_name = top_customer[0]
        top_customer_spent = top_customer[1]
        print(f"Top Spending: {top_customer_name} - R$ {top_customer_spent:,.2f}")
        dict_spending["top_spending"] = {
            "name": top_customer_name,
            "R$": top_customer_spent
        }
        mount_dict.update({"Spending": dict_spending})
        with open(os.path.join(settings.upload_files_bucket, "relatorio.json"), "w") as f:
            f.write(json.dumps(mount_dict, indent=4))
        return mount_dict


    async def generate(self):
        with open(os.path.join(os.getcwd(), settings.upload_files_bucket, "merged_files.json"), 'r') as f:
            merged = json.load(f)

        customers = self._total_order_by_customer(merged)
        country = self._total_by_contry(merged, customers)
        quantity = self._total_by_quantity(merged, country)
        return self._total_by_spending(merged, quantity)