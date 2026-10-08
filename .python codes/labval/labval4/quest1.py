
catalogo={
"arroz":12.50,
"feijao":8.90,
"macarrao":5.25,
"carne":25.00,
"frango":18.75,
"ovo":3.50,
"leite":4.20,
"pao":2.80,
}
item_buscado=input("digite o produto que dejesa buscar: ").strip().lower()
if item_buscado in catalogo:
    preco=catalogo[item_buscado]
    print(f"o produto foi encontrado! o preco de {item_buscado} e {preco:2f}")
else:
    print(f"o produto {item_buscado} nao foi encontrado!")