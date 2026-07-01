from flask import Blueprint, request, jsonify
from services.scan_service import validate_barcode
from services.product_service import get_product

scan_bp = Blueprint("scan", __name__)


@scan_bp.route("/scan", methods=["POST"])
def scan():
    # 사용자가 보낸 JSON 데이터 받기
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "JSON body가 필요합니다."
        }), 400

    # barcode 값 추출
    barcode = data.get("barcode")

    # barcode 값 검증
    is_valid, message = validate_barcode(barcode)

    if not is_valid:
        return jsonify({
            "error": message
        }), 400

    
    product = get_product(barcode)
  
    if product is None:
        return jsonify({
            "error": "상품을 찾을 수 없습니다."
        }), 404


    return jsonify({
        "barcode" : barcode,
        "product" : product
        })
